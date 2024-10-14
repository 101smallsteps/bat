from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.conf import settings  # For email configurations
from django.core.mail import send_mail
from .serializers import (
    RegisteredInstitutionSerializer,TeamSerializer,JobSerializer, StaffApplicationSerializer, UserDetailsSerializer,
    TaskSerializer, TaskCommentSerializer, ContributionSerializer, TaskListSerializer,
    ProjectSerializer,TaskOwnershipHistorySerializer
)
from .models import Team,TaskOwnershipHistory,RegisteredInstitution,Project,Job, StaffApplication, UserDetails, Task, TaskComment, Contribution, DesignationHistory, TaskList
from financials.models import Symbol
from financials.serializers import SymbolSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from django.db.models import Q
import logging
from django.db.models import Avg

# Create a logger for this module
logger = logging.getLogger(__name__)

class RegisteredInstitutionViewSet(viewsets.ModelViewSet):
    queryset = RegisteredInstitution.objects.all()
    serializer_class = RegisteredInstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = []  # Adjust permissions as needed

    def perform_create(self, serializer):
        # Custom creation behavior
        serializer.save(created_on=timezone.now())  # Set the created_on date


    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        # Custom endpoint to activate a team
        team = self.get_object()
        team.is_active = True
        team.save()
        return Response({'status': 'team activated'})

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        # Custom endpoint to close a team
        team = self.get_object()
        team.is_active = False
        team.closed_on = timezone.now()
        team.save()
        return Response({'status': 'team closed'})

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]  # Or any other permissions as needed

    # You can override create and update methods if specific logic is required
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
class UnassignedSymbolListView(generics.ListAPIView):
    serializer_class = SymbolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assigned_symbols = UserDetails.objects.values_list('symbol', flat=True)
        return Symbol.objects.exclude(id__in=assigned_symbols)


# List view for all jobs
class JobsListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# StaffApplication view set
class StaffApplicationViewSet(viewsets.ModelViewSet):
    queryset = StaffApplication.objects.all()
    serializer_class = StaffApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Retrieve the job ID from the validated data
        job_id = self.request.data.get('job')
        if job_id:
            try:
                # Get the Job instance based on the ID
                job_instance = Job.objects.get(id=job_id)
            except Job.DoesNotExist:
                raise serializers.ValidationError({"job": "Invalid job ID."})

            # Save the application with the job instance
            serializer.save(user=self.request.user, job=job_instance)
        else:
            raise serializers.ValidationError({"job": "This field is required."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        application = self.get_object()
        if not request.user.is_superuser:
            return Response({'detail': 'Only superusers can approve applications.'}, status=status.HTTP_403_FORBIDDEN)
        if application.approved:
            return Response({'detail': 'Application already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        symbol_id = request.data.get('symbol_id')
        job_id = application.job_id

        if not symbol_id:
            return Response({'detail': 'Symbol ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            symbol = Symbol.objects.get(id=symbol_id)
        except Symbol.DoesNotExist:
            return Response({'detail': 'Invalid Symbol ID.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job = Job.objects.get(id=job_id)
            designation = job.designation
            designation_level = job.designation_level
        except Job.DoesNotExist:
            return Response({'detail': 'Invalid Job ID.'}, status=status.HTTP_400_BAD_REQUEST)

        application.approved = True
        application.save()
        user = application.user
        user.is_staff = True
        user.save()

        UserDetails.objects.update_or_create(
            user=application.user,
            defaults={
                'symbol': symbol,
                'institution_name': application.institution_name,
                'home_address': application.home_address,
                'current_designation': designation,
                'current_designation_level': designation_level,
                'approved_at': timezone.now(),
            }
        )
        self.update_designation_history(application.user, designation, designation_level)
        return Response({'detail': 'Application approved and symbol assigned.'})

    def update_designation_history(self, user, new_designation, new_level):
        current_history = DesignationHistory.objects.filter(user=user, designation_ended__isnull=True).first()
        if current_history:
            current_history.designation_ended = timezone.now().date()
            current_history.save()

        DesignationHistory.objects.create(
            user=user,
            designation=new_designation,
            designation_level=new_level,
            designation_started=timezone.now().date()
        )
        user_details = UserDetails.objects.get(user=user)
        user_details.current_designation = new_designation
        user_details.current_designation_level = new_level
        user_details.save()



class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>[^/.]+)')
    def retrieve_by_user(self, request, user_id=None):
        # Try to fetch UserDetails for the provided user_id
        user_details = self.queryset.filter(user__id=user_id).first()
        if not user_details:
            raise NotFound("User details not found.")
        serializer = self.get_serializer(user_details)
        return Response(serializer.data)

# UserDetails view set
class UserDetailsViewSet_old(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter based on the user ID passed as input
        user_id = self.kwargs.get('user_id') or self.request.user.id  # Fallback to current user ID if none provided
        return UserDetails.objects.filter(user__id=user_id)

    def retrieve(self, request, *args, **kwargs):
        # Override retrieve to filter by the user id directly
        queryset = self.get_queryset()
        user_details = queryset.first()  # Should only retrieve one result since it's a one-to-one relationship
        if not user_details:
            raise NotFound("User details not found.")
        serializer = self.get_serializer(user_details)
        return Response(serializer.data)


# TaskList view set
class TaskListViewSet(viewsets.ModelViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        tasklist = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(TaskList.STATUS_CHOICES):
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        tasklist.status = new_status
        tasklist.save()
        return Response({'detail': f'Task list status changed to {new_status}.'})


# Task view set
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('assigned_to')
        if user_id:
            return self.queryset.filter(Q(assigned_to=user_id) | Q(task_credit_owner=user_id))
        return self.queryset

    @action(detail=False, methods=['get'], url_path='user-history-completed-accepted')
    def user_history_completed_accepted(self, request):
        """
        Retrieve tasks that are in completed or accepted state for a specific user
        based on their history in TaskOwnershipHistory.
        """
        user = request.user
        tasks = Task.objects.filter(
            Q(ownership_history__user=user) &
            Q(task_status__in=['completed', 'accepted'])
        ).distinct()

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user-closed-tasks')
    def user_closed_tasks(self, request):
        # Get the current user
        user = request.user

        # Query TaskOwnershipHistory to find closed tasks for the user
        closed_tasks = Task.objects.filter(
            ownership_history__user=user,
            task_status='closed'
        ).distinct()

        # Serialize and return the tasks
        serializer = self.get_serializer(closed_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_user_ratings(self,user_details):
        # Aggregate rating for this user’s contributions
        avg_rating = Contribution.objects.filter(user=user_details.user).aggregate(Avg('rating'))['rating__avg'] or 0
        stars = int(avg_rating)  # One star for each point of average rating

        # Update and save cached fields
        user_details.average_rating = avg_rating
        user_details.stars = stars
        user_details.save()


    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get("task_status")
        completion_summary = request.data.get("completion_summary")

        # Ensure task status and completion summary are updated
        if new_status:
            task.task_status = new_status
            if new_status == 'completed':
                task.completed_at = timezone.now()
                if task.task_creator:
                    task.assigned_to = task.task_creator
                    task._assigned_by = request.user
                    # Record ownership change in TaskOwnershipHistory
#                    TaskOwnershipHistory.objects.create(
#                        task=task,
#                        user=task.task_creator,
#                        assigned_by=request.user  # Tracks who made the assignment
#                    )
            if new_status == 'started':
                task.started_at = timezone.now()
            if new_status == 'accepted':
                task.accepted_at = timezone.now()
            if new_status == 'closed':
                task.closed_at = timezone.now()
                self.get_serializer().update_rating(task)
                # Apply rating to all users in TaskOwnershipHistory
                involved_users = TaskOwnershipHistory.objects.filter(task=task).values_list('user',
                                                                                            flat=True).distinct()
                for user_id in involved_users:
                    user = User.objects.get(id=user_id)

                    # Update or create Contribution for each user
                    Contribution.objects.update_or_create(
                        user=user,
                        task=task,
                        defaults={
                            'rating': task.rating,
                            'rating_summary': task.rating_summary or "No summary provided",
                            'submitted_at': timezone.now()  # Set submission time if necessary
                        }
                    )

                    # Update the UserDetails cache for each user
                    user_details, created = UserDetails.objects.get_or_create(user=user)
                    self.update_user_ratings(user_details)
            if completion_summary:
                task.completion_summary = completion_summary
            task.save()
            return Response({"status": "Task status updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # Fetch tasks assigned to the user based on type
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        task = self.get_object()
        if task.task_status != 'created':
            return Response({'error': 'Task must be in "created" status to start.'}, status=status.HTTP_400_BAD_REQUEST)

        task.task_status = 'started'
        task.started_at = timezone.now()  # Capture start time
        task.save()
        return Response({'status': 'Task started'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def assign_task(self, request, pk=None):
        task = self.get_object()
        new_assignee_id = request.data.get('assigned_to_id')

        if not new_assignee_id:
            return Response({"error": "assigned_to_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_assignee_id != task.assigned_to.id:
            # Get new user instance
            new_assignee = User.objects.get(id=new_assignee_id)
            task.assigned_to = new_assignee
            task._assigned_by = request.user
            task.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.task_status != 'started':
            return Response({'error': 'Task must be in "started" status to complete.'},
                            status=status.HTTP_400_BAD_REQUEST)

        task.task_status = 'completed'
        task.completed_at = timezone.now()  # Capture completion time
        task.save()
        return Response({'status': 'Task completed'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def live_tasks(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user, task_type='sequential', task_status__in=['assigned', 'started'])
        return Response(self.get_serializer(tasks, many=True).data)

    @action(detail=False, methods=['get'])
    def planned_tasks(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user, task_status__in=['created', 'assigned', 'started'])
        return Response(self.get_serializer(tasks, many=True).data)

    @action(detail=False, methods=['get'])
    def out_of_order_tasks(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user, task_type='out_of_order', task_status__in=['created', 'assigned', 'started'])
        return Response(self.get_serializer(tasks, many=True).data)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get("task_status")
        rollback_reason = request.data.get("rollback_reason", "")

        # Use the serializer to handle validation and update
        serializer = TaskSerializer(task, data={"task_status": new_status, "rollback_reason": rollback_reason}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def completed_tasks(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user, task_status='completed')
        return Response(self.get_serializer(tasks, many=True).data)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        task = self.get_object()
        if task.task_status != 'completed':
            return Response({'error': 'Task must be "completed" before it can be accepted.'},
                            status=status.HTTP_400_BAD_REQUEST)

        task.task_status = 'accepted'
        task.accepted_at = timezone.now()  # Capture accepted time
        task.save()
        return Response({'status': 'Task accepted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        task = self.get_object()
        if task.task_status != 'accepted':
            return Response({'error': 'Task must be "accepted" before it can be closed.'},
                            status=status.HTTP_400_BAD_REQUEST)

        task.task_status = 'closed'
        task.closed_at = timezone.now()  # Capture close time
        task.save()
        return Response({'status': 'Task closed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        task = self.get_object()
        if not task.completed:
            return Response({'detail': 'Task is not completed.'}, status=status.HTTP_400_BAD_REQUEST)
        task.completed = False
        task.completed_at = None
        task.save()
        return Response({'detail': 'Task reopened.'})

class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_pk') or self.request.data.get('task')
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise ValidationError({"task": "The specified task does not exist."})

        serializer.save(user=self.request.user, task=task)

class TaskCompleteViewSet(viewsets.ViewSet):
        """
        A viewset for task completion and related actions.
        """

        @action(detail=True, methods=['post'])
        def complete_task(self, request, pk=None):
            """
            Mark a task as completed with an optional summary and evidence.
            """
            task = Task.objects.get(pk=pk)
            task.task_status = 'completed'
            task.completed_at = timezone.now()
            task.completion_summary = request.data.get('completion_summary', '')

            # Handle completion evidence if provided
            evidence = request.FILES.get('completion_evidence')
            if evidence:
                task.completion_evidence = evidence

            task.save()
            return Response({'status': 'Task marked as completed'}, status=status.HTTP_200_OK)

        @action(detail=True, methods=['post'])
        def add_comment(self, request, pk=None):
            """
            Add a comment to the specified task.
            """
            task = Task.objects.get(pk=pk)
            comment_data = {
                'task': task.id,
                'user': request.user.id,
                'comment': request.data.get('comment')
            }
            serializer = TaskCommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Contribution view set
class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskOwnershipHistoryViewSet_old(viewsets.ReadOnlyModelViewSet):
    queryset = TaskOwnershipHistory.objects.all()
    serializer_class = TaskOwnershipHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by user or task.
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        task_id = self.request.query_params.get('task_id')

        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if task_id:
            queryset = queryset.filter(task__id=task_id)

        return queryset

class TaskOwnershipHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskOwnershipHistory.objects.all()
    serializer_class = TaskOwnershipHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>[^/.]+)')
    def retrieve_by_user(self, request, user_id=None):
        # Filter TaskOwnershipHistory entries by user_id
        task_history = self.queryset.filter(user__id=user_id)
        if not task_history.exists():
            raise NotFound("No task ownership history found for the user.")
        serializer = self.get_serializer(task_history, many=True)
        return Response(serializer.data)