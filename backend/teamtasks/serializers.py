from rest_framework import serializers
from .models import Project, Job, StaffApplication, UserDetails, Task, TaskComment, Contribution,DesignationHistory
from certification.models import CertificateType  # Assuming CertificateType is in the certification app

# Serializer for Project
class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(many=True)  # You can customize this to include user details if needed

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'project_type', 'users']

class CertificateTypeSerializer(serializers.ModelSerializer):
    quiz_name = serializers.CharField(source="quiz.name", read_only=True)

    class Meta:
        model = CertificateType
        fields = ['id', 'name', 'quiz_name']  # Adjust fields as necessary

# Serializer for Job
class JobSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()  # Nested Project details
    prerequisites = CertificateTypeSerializer(many=True)  # CertificateType related to the job

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'responsibilities', 'prerequisites', 'project','designation','designation_level']

# Serializer for StaffApplication
class StaffApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Simplified, you can customize to return more user details
    #job = JobSerializer()  # Nested Job details
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
    user = serializers.StringRelatedField()  # Simplified for now

    class Meta:
        model = UserDetails
        fields = ['id', 'user', 'symbol', 'home_address', 'institution_address']

class DesignationHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Or use `PrimaryKeyRelatedField` for user ID

    class Meta:
        model = DesignationHistory
        fields = ['id', 'user', 'designation', 'designation_level', 'designation_started', 'designation_ended']
        read_only_fields = ['designation_started']  # Assuming designation start date is set automatically
2.
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        # If task is sequential, ensure previous_task is set
        if data['task_type'] == 'sequential' and not data.get('previous_task'):
            raise serializers.ValidationError("Sequential tasks must have a previous task.")
        return data

# Serializer for TaskComment
class TaskCommentSerializer(serializers.ModelSerializer):
    task = TaskSerializer()  # Nested task details
    user = serializers.StringRelatedField()

    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'user', 'comment', 'created_at']


# Serializer for Contribution
class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    task = TaskSerializer()

    class Meta:
        model = Contribution
        fields = ['id', 'user', 'task', 'submitted_at']
