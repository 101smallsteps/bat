from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import JobSerializer, StaffApplicationSerializer, UserDetailsSerializer, TaskSerializer, TaskCommentSerializer
from .models import Job,StaffApplication, UserDetails, Task, TaskComment,DesignationHistory
from financials.models import Symbol  # Import the Symbol model
from financials.serializers import SymbolSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings  # Import settings for email configuration
from django.utils import timezone  # Import timezone for date handling
# from .tasks import send_disapproval_email  # Uncomment if using Celery for email tasks
from rest_framework import generics


class UnassignedSymbolListView(generics.ListAPIView):
    serializer_class = SymbolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve symbols that are not assigned to any user in UserDetails
        assigned_symbols = UserDetails.objects.values_list('symbol', flat=True)
        return Symbol.objects.exclude(id__in=assigned_symbols)


# List view for all jobs
class JobsListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
class StaffApplicationViewSet(viewsets.ModelViewSet):
    queryset = StaffApplication.objects.all()
    serializer_class = StaffApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print("Serializer Errors:", serializer.errors)  # Log the errors for detailed info
            raise serializers.ValidationError(serializer.errors)  # Ensure the error is included in the response

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])  # Only superusers can approve
    def approve(self, request, pk=None):
        print(f"User: {request.user}, Is SuperUser: {request.user.is_superuser}")

        application = self.get_object()

        if not request.user.is_superuser:
            return Response({'detail': 'Only superusers can approve applications.'}, status=status.HTTP_403_FORBIDDEN)

        if application.approved:
            return Response({'detail': 'Application already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the symbol ID is passed in the request data
        symbol_id = request.data.get('symbol_id')
        job_id =  application.job_id  # Get job ID from the request data

        if not symbol_id:
            return Response({'detail': 'Symbol ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            symbol = Symbol.objects.get(id=symbol_id)  # Get the symbol by ID
        except Symbol.DoesNotExist:
            return Response({'detail': 'Invalid Symbol ID.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job = Job.objects.get(id=job_id)  # Get the job by job ID
            designation = job.designation  # Fetch designation from Job
            designation_level = job.designation_level  # Fetch designation level from Job
        except Job.DoesNotExist:
            return Response({'detail': 'Invalid Job ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Approve the application and assign the selected symbol
        application.approved = True
        application.save()

        # Mark the user as staff
        user = application.user
        user.is_staff = True
        user.save()

        # Update or create UserDetails
        UserDetails.objects.update_or_create(
            user=application.user,
            defaults={
                'symbol': symbol,
                'institution_name': application.institution_name,
                'home_address': application.home_address,
                'home_state': application.home_state,
                'home_county': application.home_county,
                'home_country': application.home_country,
                'home_zipcode': application.home_zipcode,
                'institution_address': application.institution_address,
                'institution_state': application.institution_state,
                'institution_county': application.institution_county,
                'institution_country': application.institution_country,
                'institution_zipcode': application.institution_zipcode,
                'email': application.email,
                'phone': application.phone,
                'current_designation': designation,
                'current_designation_level': designation_level,
                'approved_at': timezone.now(),
            }
        )
        self.update_designation_history(application.user,designation,designation_level)
        return Response({'detail': 'Application approved and symbol assigned.'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])  # Only superusers can disapprove
    def disapprove(self, request, pk=None):
        application = self.get_object()
        if application.approved:
            return Response({'detail': 'Application already approved.'}, status=status.HTTP_400_BAD_REQUEST)
        # You can use Celery for sending an email if needed
        send_mail(
            'Application Disapproved',
            'Your staff application has been disapproved. Please contact us for more information.',
            settings.DEFAULT_FROM_EMAIL,
            [application.user.email],
            fail_silently=False,
        )
        application.delete()
        return Response({'detail': 'Application disapproved and email sent.'})

    def update_designation_history(self,user, new_designation, new_level):

        # End the current designation in history, if it exists
        current_history = DesignationHistory.objects.filter(user=user, designation_ended__isnull=True).first()
        if current_history:
            current_history.designation_ended = timezone.now().date()
            current_history.save()

        # Add a new designation history entry
        DesignationHistory.objects.create(
            user=user,
            designation=new_designation,
            designation_level=new_level,
            designation_started=timezone.now().date()
        )

        # Update UserDetails to reflect the current designation
        user_details = UserDetails.objects.get(user=user)
        user_details.current_designation = new_designation
        user_details.current_designation_level = new_level
        user_details.designation_started = timezone.now().date()
        user_details.save()
class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.completed:
            return Response({'detail': 'Task already completed.'}, status=status.HTTP_400_BAD_REQUEST)
        task.completed = True
        task.completed_at = timezone.now()  # Use timezone.now() for the timestamp
        task.save()
        return Response({'detail': 'Task marked as complete.'})

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        task = self.get_object()
        if not task.completed:
            return Response({'detail': 'Task is not completed.'}, status=status.HTTP_400_BAD_REQUEST)
        task.completed = False
        task.completed_at = None  # Clear completed timestamp
        task.save()
        return Response({'detail': 'Task reopened.'})

class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
