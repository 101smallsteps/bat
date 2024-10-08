from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import JobSerializer, StaffApplicationSerializer, UserDetailsSerializer, TaskSerializer, TaskCommentSerializer
from .models import Job,StaffApplication, UserDetails, Task, TaskComment
from financials.models import Symbol  # Import the Symbol model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings  # Import settings for email configuration
from django.utils import timezone  # Import timezone for date handling
# from .tasks import send_disapproval_email  # Uncomment if using Celery for email tasks
from rest_framework import generics

# List view for all jobs
class JobsListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
class StaffApplicationViewSet(viewsets.ModelViewSet):
    queryset = StaffApplication.objects.all()
    serializer_class = StaffApplicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print("Serializer Errors:", serializer.errors)  # Log the errors for detailed info
            raise serializers.ValidationError(serializer.errors)  # Ensure the error is included in the response

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])  # Only superusers can approve
    def approve(self, request, pk=None):
        application = self.get_object()
        if application.approved:
            return Response({'detail': 'Application already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the symbol ID is passed in the request data
        symbol_id = request.data.get('symbol_id')
        if not symbol_id:
            return Response({'detail': 'Symbol ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            symbol = Symbol.objects.get(id=symbol_id)  # Get the symbol by ID
        except Symbol.DoesNotExist:
            return Response({'detail': 'Invalid Symbol ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Approve the application and assign the selected symbol
        application.approved = True
        application.save()

        # Create UserDetails with the assigned symbol and other details
        UserDetails.objects.create(
            user=application.user,
            symbol=symbol,
            home_address=application.home_address,
            school_address=application.school_address
        )

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
