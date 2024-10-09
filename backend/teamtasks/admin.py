from django.contrib import admin
from .models import Project, Job, StaffApplication, UserDetails, Task, TaskComment, Contribution,DesignationHistory

# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'start_date', 'end_date')
    list_filter = ('project_type',)
    search_fields = ('title', 'description')
    filter_horizontal = ('users',)  # Allows for multi-selection for many-to-many fields

# Job Admin
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'project','designation','designation_level')
    list_filter = ('project',)
    search_fields = ('title', 'description', 'responsibilities')
    filter_horizontal = ('prerequisites',)  # Allows for multi-selection for many-to-many fields

# Staff Application Admin
@admin.register(StaffApplication)
class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'institution_name', 'job', 'approved', 'generated_at', 'approved_at')
    list_filter = ('approved', 'institution_state', 'generated_at')
    search_fields = ('user__username', 'institution_name', 'job__title', 'email', 'phone')
    readonly_fields = ('confirmation_id', 'generated_at', 'approved_at')

# User Details Admin
@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol')
    search_fields = ('user__username',)
    readonly_fields = ('user',)  # Useful if user should not change once set

@admin.register(DesignationHistory)
class DesignationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'designation_level', 'designation_started', 'designation_ended')
    list_filter = ('designation', 'designation_level', 'designation_started', 'designation_ended')
    search_fields = ('user__username', 'designation', 'designation_level')
    date_hierarchy = 'designation_started'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'assigned_to',
        'priority',
        'task_type',
        'task_status',  # New field for task status
        'completed',
        'created_at',
        'completed_at',
        'expected_completed_date',  # New field for expected completion date
        'rating'  # New field for rating
    )
    list_filter = ('priority', 'task_type', 'task_status', 'completed')  # Filter by task status
    search_fields = ('title', 'description', 'assigned_to__username')
    autocomplete_fields = ('previous_task',)  # Allows easier selection of related tasks

    # Display new fields in the admin form view
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'description',
                'assigned_to',
                'priority',
                'task_type',
                'task_status',
                'expected_completed_date',
                'expected_outcome',
                'previous_task',
            )
        }),
        ('Completion Details', {
            'fields': (
                'completed',
                'completion_summary',
                'completion_evidence',
                'completed_at',
                'rating',
            ),
            'classes': ('collapse',),  # Collapse section for cleanliness
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'completed_at')  # Make timestamps read-only


# Task Comment Admin
@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    search_fields = ('task__title', 'user__username', 'comment')
    readonly_fields = ('created_at',)

# Contribution Admin
@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'submitted_at')
    search_fields = ('user__username', 'task__title')
    readonly_fields = ('submitted_at',)
