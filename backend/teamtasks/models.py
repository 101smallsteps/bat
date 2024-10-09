from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid  # For generating unique confirmation IDs
from django.contrib.auth.models import User
from financials.models import Symbol  # Import the Symbol model
from certification.models import CertificateType
from django.utils import timezone

# Model to handle staff applications
class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('shortTerm', 'Short Term'),
        ('longTerm', 'Long Term'),
        ('continuous', 'Continuous'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # End date can be null for continuous projects
    project_type = models.CharField(max_length=15, choices=PROJECT_TYPE_CHOICES)
    users = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.title

# Define choices for designation levels and types
class Designation(models.TextChoices):
    ANALYST = 'Analyst', 'Analyst'
    PROGRAM_MANAGER = 'Program Manager', 'Program Manager'
    SENIOR_MANAGER = 'Resarcher', 'Resarcher'

class DesignationLevel(models.TextChoices):
    BEGINNER = 'Beginner', 'Beginner'
    INTERMEDIATE = 'Intermediate', 'Intermediate'
    ADVANCED = 'Advanced', 'Advanced'

class Job(models.Model):
    project = models.ForeignKey(Project, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    responsibilities = models.TextField()
    prerequisites = models.ManyToManyField(CertificateType, related_name='jobs')
    # Using choice fields for designation and level
    designation = models.CharField(max_length=50,choices=Designation.choices,blank=True,null=True)
    designation_level = models.CharField(max_length=20,choices=DesignationLevel.choices,blank=True,null=True)

    def __str__(self):
        return f"{self.title} - {self.project.title}"

class StaffApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,null=True)  # Link to the Job class
    institution_name = models.CharField(max_length=255)
    home_address = models.TextField()
    home_state = models.CharField(max_length=100)
    home_county = models.CharField(max_length=100)
    home_country = models.CharField(max_length=100)
    home_zipcode = models.CharField(max_length=10)
    institution_address = models.TextField()
    institution_state = models.CharField(max_length=100)
    institution_county = models.CharField(max_length=100)
    institution_country = models.CharField(max_length=100)
    institution_zipcode = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    approved = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the application was created
    approved_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the application was approved
    confirmation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique ID for application confirmation

    def __str__(self):
        return f"{self.user.username} - {self.institution_name} - {self.job.title}"
# Model to store additional user details including assigned symbols

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey('financials.Symbol', on_delete=models.CASCADE, null=True, blank=True)
    institution_name = models.CharField(max_length=255)
    home_address = models.TextField()
    home_state = models.CharField(max_length=100)
    home_county = models.CharField(max_length=100)
    home_country = models.CharField(max_length=100)
    home_zipcode = models.CharField(max_length=10)
    institution_address = models.TextField()
    institution_state = models.CharField(max_length=100)
    institution_county = models.CharField(max_length=100)
    institution_country = models.CharField(max_length=100)
    institution_zipcode = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    approved_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the application was approved

    # Using choice fields for designation and level
    current_designation = models.CharField(
        max_length=50,
        choices=Designation.choices,
        blank=True,
        null=True
    )
    current_designation_level = models.CharField(
        max_length=20,
        choices=DesignationLevel.choices,
        blank=True,
        null=True
    )
    designation_started = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_current_designation_display()}"


class DesignationHistory(models.Model):
    user = models.ForeignKey(User, related_name='designation_history', on_delete=models.CASCADE)
    designation = models.CharField(max_length=50, choices=Designation.choices)
    designation_level = models.CharField(max_length=20, choices=DesignationLevel.choices)
    designation_started = models.DateField(default=timezone.now)
    designation_ended = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-designation_started']

    def __str__(self):
        return f"{self.user.username} - {self.designation} ({self.designation_level})"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    TASK_TYPE_CHOICES = [
        ('sequential', 'Sequential'),
        ('parallel', 'Parallel'),
        ('out_of_order', 'Out of Order'),
    ]

    STATUS_CHOICES = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('accepted', 'Accepted'),
        ('closed', 'Closed'),
    ]

    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    # Task priority and type
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='sequential')

    # Sequential task dependency
    previous_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_tasks')

    # Additional fields
    expected_completed_date = models.DateField(null=True, blank=True)
    expected_outcome = models.TextField(null=True, blank=True)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    rating = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5

    # Completion details
    completion_summary = models.TextField(null=True, blank=True)
    completion_evidence = models.ImageField(upload_to='task_evidence/', null=True, blank=True)  # Path to save images

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def can_start(self):
        if self.task_type == 'sequential' and self.previous_task:
            return self.previous_task.completed
        return True

    def __str__(self):
        return self.title
class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"Comment on {self.task.title} by {self.user.username}"

# Model to track contributions (completed tasks)
class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

