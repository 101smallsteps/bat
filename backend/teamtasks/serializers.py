from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone


from .models import (
    RegisteredInstitution,Team,TaskOwnershipHistory,Project, Job, StaffApplication, UserDetails, Task, TaskComment, Contribution,
    DesignationHistory, TaskList
)
from certification.models import CertificateType  # Assuming CertificateType is in the certification app
import logging
# Create a logger for this module
logger = logging.getLogger(__name__)
class RegisteredInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredInstitution
        fields = [
            'id', 'name', 'address', 'country', 'zipcode',
            'is_college', 'is_school', 'is_organisation',
            'website', 'email'
        ]
class TeamSerializer(serializers.ModelSerializer):
    leaders = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True)
    institution = serializers.PrimaryKeyRelatedField(queryset=RegisteredInstitution.objects.all(), allow_null=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'team_type', 'leaders', 'members', 'projects', 'institution',
            'is_institution', 'created_on', 'closed_on', 'is_active'
        ]
        read_only_fields = ['created_on']  # Only editable on creation
# Serializer for CertificateType
class CertificateTypeSerializer(serializers.ModelSerializer):
    quiz_name = serializers.CharField(source="quiz.name", read_only=True)

    class Meta:
        model = CertificateType
        fields = ['id', 'name', 'quiz_name']


# Serializer for Project
class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'
# Serializer for Job
class JobSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()  # Nested Project details
    prerequisites = CertificateTypeSerializer(many=True)  # Nested CertificateType related to the job

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'responsibilities', 'prerequisites', 'project', 'designation', 'designation_level']


# Serializer for StaffApplication
class StaffApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Simplified user details (username)
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())

    class Meta:
        model = StaffApplication
        fields = [
            'id', 'user', 'job', 'institution_name', 'home_address', 'home_state', 'home_county',
            'home_country', 'home_zipcode', 'institution_address', 'institution_state',
            'institution_county', 'institution_country', 'institution_zipcode', 'email', 'phone',
            'approved', 'generated_at', 'approved_at', 'confirmation_id'
        ]


# Serializer for UserDetails
class UserDetailsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Username only

    class Meta:
        model = UserDetails
        fields = [
            'id', 'user', 'symbol', 'institution_name', 'home_address', 'home_state', 'home_county',
            'home_country', 'home_zipcode', 'institution_address', 'institution_state',
            'institution_county', 'institution_country', 'institution_zipcode', 'email', 'phone',
            'approved_at', 'current_designation', 'current_designation_level', 'designation_started',
            'average_rating','stars'
        ]


# Serializer for DesignationHistory
class DesignationHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Username only

    class Meta:
        model = DesignationHistory
        fields = ['id', 'user', 'designation', 'designation_level', 'designation_started', 'designation_ended']
        read_only_fields = ['designation_started']


# Serializer for TaskList
class TaskListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    owners = serializers.StringRelatedField(many=True)  # Username only

    class Meta:
        model = TaskList
        fields = [
            'id', 'project', 'name', 'type', 'start_date', 'end_date', 'owners',
            'status', 'rating', 'rating_summary'
        ]


class TaskOwnershipHistorySerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    assigned_by = serializers.StringRelatedField()

    class Meta:
        model = TaskOwnershipHistory
        fields = ['id', 'task', 'user', 'assigned_at', 'assigned_by']


class TaskCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Username only
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'user', 'comment', 'created_at']


# Serializer for Task
class TaskSerializer(serializers.ModelSerializer):
    task_list = TaskListSerializer()
    subtask_list = TaskListSerializer(required=False)  # Nested TaskList for subtasks, optional
    assigned_to = serializers.StringRelatedField()  # Username only
    ownership_history = TaskOwnershipHistorySerializer(many=True, read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['assigned_to','ownership_history']  # Prevent external updates

    def update(self, instance, validated_data):
        # Retrieve the new status and current status
        new_status = validated_data.get("task_status", instance.task_status)
        rollback_reason = validated_data.get("rollback_reason", "")

        # Define allowed transitions
        allowed_transitions = {
            'created': ['assigned'],
            'assigned': ['started'],
            'reopened': ['started'],
            'started': ['completed'],
             'completed': ['accepted', 'assigned','reopened'],
            'accepted': ['closed'],
            'closed': []
        }

        if new_status not in allowed_transitions[instance.task_status]:
            raise serializers.ValidationError(
                f"Transition from {instance.task_status} to {new_status} is not allowed."
            )

        # If rolling back to 'started', a rollback reason is required
        if new_status == 'started' and instance.task_status == 'completed':
            if not rollback_reason:
                raise serializers.ValidationError("A rollback reason is required to move from completed to started.")
            self.notify_user(instance.assigned_to, rollback_reason)

        # Set the appropriate timestamp for the new status
        if new_status == 'started' and instance.started_at is None:
            instance.started_at = timezone.now()
        elif new_status == 'completed' and instance.completed_at is None:
            instance.completed_at = timezone.now()
        elif new_status == 'accepted' and instance.accepted_at is None:
            instance.accepted_at = timezone.now()
        elif new_status == 'closed' and instance.closed_at is None:
            instance.closed_at = timezone.now()
            logger.debug("closed and about to call update_rating")
            self.update_rating(instance)  # Update rating on completion

        instance.rollback_reason = rollback_reason
        instance.save()
        return super().update(instance, validated_data)

    def validate(self, data):
        # Validate sequential task requirements
        if data['task_type'] == 'sequential' and not data.get('previous_task'):
            raise serializers.ValidationError("Sequential tasks must have a previous task.")
        return data

    def notify_user(self, user: User, reason: str):
        # Send a notification email to the assigned user
        send_mail(
            'Task Status Update Notification',
            f'Dear {user.username},\n\nThe status of your task has been changed to "started" due to the following reason:\n\n{reason}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

    def update_rating(self, instance):
        """
        Update the rating of the task based on how promptly it was completed.
        """
        logger.debug(f"at update_rating - {instance.expected_completed_date} and {instance.completed_at}")

        if instance.expected_completed_date and instance.completed_at:
            days_late = (instance.completed_at.date() - instance.expected_completed_date).days
            logger.debug(f"at update_rating -days_late - {days_late} ")

            # Determine the rating based on how late the task was completed
            if days_late <= 0:
                instance.rating = 5
            elif days_late == 2:
                instance.rating = 4
            elif days_late == 3:
                instance.rating = 3
            elif days_late == 5:
                instance.rating = 2
            elif days_late >= 6:
                instance.rating = 1
            else:
                instance.rating = 0

            instance.save()  # Save the updated rating

        # Update or create a Contribution record
        Contribution.objects.update_or_create(
            user=instance.assigned_to,
            task=instance,
            defaults={
                'rating': instance.rating,
                'rating_summary': instance.rating_summary or "No summary provided",
                'submitted_at': timezone.now()  # Update submission time if necessary
            }
        )
# Serializer for TaskComment

# Serializer for Contribution
class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Username only
    task = TaskSerializer()

    class Meta:
        model = Contribution
        fields = ['id', 'user', 'task', 'submitted_at']
