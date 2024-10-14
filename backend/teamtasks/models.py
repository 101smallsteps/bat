from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid  # For generating unique confirmation IDs
from django.contrib.auth.models import User
from financials.models import Symbol  # Import the Symbol model
from certification.models import CertificateType
from django.utils import timezone


class RegisteredInstitution(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)

    # New fields
    is_college = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)
    is_organisation = models.BooleanField(default=False)
    website = models.URLField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

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

class Team(models.Model):
    TEAM_TYPE_CHOICES = [
        ('BatAdminNational', 'BatAdminNational'),
        ('BatAdminState', 'BatAdminState'),
        ('BatAdminDistrict', 'BatAdminDistrict'),
        ('BatAdminCounty', 'BatAdminCounty'),
        ('BatAnalyst', 'BatAnalyst'),
        ('BatAmbassador', 'BatAmbassador'),
        ('Club', 'Club'),
    ]

    name = models.CharField(max_length=255)
    team_type = models.CharField(max_length=20, choices=TEAM_TYPE_CHOICES)
    leaders = models.ManyToManyField(User, related_name='leading_teams')
    members = models.ManyToManyField(User, related_name='member_teams')
    projects = models.ManyToManyField(Project, related_name='teams')

    # Institution-related fields
    institution = models.ForeignKey(
        RegisteredInstitution,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='teams'
    )
    is_institution = models.BooleanField(default=False)

    # New fields
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    closed_on = models.DateTimeField(null=True, blank=True)  # Can be set when the team is closed
    is_active = models.BooleanField(default=False)  # Set to False by default

    def __str__(self):
        return self.name



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

class TaskList(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('stopped', 'Stopped'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]

    TASK_TYPE_CHOICES = [
        ('shortTerm', 'Short Term'),
        ('longTerm', 'Long Term'),
        ('continuous', 'Continuous'),
    ]

    project = models.ForeignKey(Project, related_name='tasklists', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=TASK_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    owners = models.ManyToManyField(User, related_name='owned_tasklists')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    rating = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)])
    rating_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.project.title}"
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
    designation_started = models.DateField(null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    stars = models.PositiveIntegerField(default=0)

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
        ('reopened', 'Reopened'),
        ('assigned', 'Assigned'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('accepted', 'Accepted'),
        ('closed', 'Closed'),
    ]

    task_list = models.ForeignKey(TaskList, related_name='tasks', on_delete=models.CASCADE)
    task_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_tasks',null=True)  # Set related_name
#    task_credit_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_owned_tasks')  # Set related_name
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')  # Set related_name
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    # Subtask list, if this task has subtasks
    subtask_list = models.ForeignKey(TaskList, on_delete=models.SET_NULL, null=True, blank=True, related_name='parent_task')

    # Task priority and type
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='sequential')

    # Sequential task dependency
    previous_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_tasks')

    # Additional fields
    expected_completed_date = models.DateField(null=True, blank=True)
    expected_outcome = models.TextField(null=True, blank=True)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    rating = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(0, 6)])  # Rating from 1 to 5
    rating_summary = models.TextField(null=True, blank=True)

    # Completion details
    completion_summary = models.TextField(null=True, blank=True)
    completion_evidence = models.ImageField(upload_to='task_evidence/', null=True, blank=True)  # Path to save images

    # Transition timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def can_start(self):
        if self.task_type == 'sequential' and self.previous_task:
            return self.previous_task.completed
        return True

    def __str__(self):
        return self.title

class TaskOwnershipHistory(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='ownership_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The new owner assigned to the task
    assigned_at = models.DateTimeField(auto_now_add=True)     # The date and time of assignment
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments_made')  # The user who made the assignment

    def __str__(self):
        return f"{self.task.title} assigned to {self.user.username} on {self.assigned_at}"

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
    rating = models.IntegerField(default=0)
    rating_summary = models.TextField(null=True, blank=True)

