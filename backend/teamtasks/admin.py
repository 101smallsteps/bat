from django.contrib import admin
from .models import TaskOwnershipHistory,Project, Job, StaffApplication, UserDetails, TaskList,Task, TaskComment, Contribution,DesignationHistory

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
    list_display = ('id','user', 'symbol')
    search_fields = ('user__username',)
    readonly_fields = ('user',)  # Useful if user should not change once set

@admin.register(DesignationHistory)
class DesignationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'designation_level', 'designation_started', 'designation_ended')
    list_filter = ('designation', 'designation_level', 'designation_started', 'designation_ended')
    search_fields = ('user__username', 'designation', 'designation_level')
    date_hierarchy = 'designation_started'

@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'type', 'start_date', 'end_date', 'status', 'rating')
    list_filter = ('status', 'type', 'start_date', 'end_date', 'rating')
    search_fields = ('name', 'project__title', 'owners__username')
    filter_horizontal = ('owners',)  # Makes selecting owners easier
    date_hierarchy = 'start_date'
    ordering = ('start_date', 'end_date')

    fieldsets = (
        (None, {
            'fields': ('project', 'name', 'type', 'start_date', 'end_date', 'status', 'owners')
        }),
        ('Rating Details', {
            'fields': ('rating', 'rating_summary')
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_status', 'priority', 'assigned_to', 'task_creator','created_at', 'completed_at')
    list_filter = ('task_status', 'priority', 'task_type', 'completed', 'assigned_to')
    search_fields = ('title', 'description', 'assigned_to__username')
    readonly_fields = ('created_at', 'started_at', 'completed_at', 'accepted_at', 'closed_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'task_list', 'assigned_to', 'completed')
        }),
        ('Task Details', {
            'fields': ('task_creator','priority', 'task_type', 'task_status', 'expected_completed_date', 'expected_outcome', 'rating', 'rating_summary')
        }),
        ('Dependencies', {
            'fields': ('previous_task', 'subtask_list')
        }),
        ('Completion Details', {
            'fields': ('completion_summary', 'completion_evidence')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at', 'accepted_at', 'closed_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Check if this is an update and if `assigned_to` has changed
        if change:  # `change` is True if this is an update, not a new object
            obj._assigned_by = request.user
#                # Create a TaskOwnershipHistory entry
#                TaskOwnershipHistory.objects.create(
#                    task=obj,
#                    user=obj.assigned_to,
#                    assigned_at=timezone.now(),
#                    assigned_by=request.user  # The admin user who made the change
#                )

        # Save the Task object as usual
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # Example: prevent deletion if the task is closed
        if obj and obj.task_status == 'closed':
            return False
        return super().has_delete_permission(request, obj)


# Task Comment Admin
@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    search_fields = ('task__title', 'user__username', 'comment')
    readonly_fields = ('created_at',)

@admin.register(TaskOwnershipHistory)
class TaskOwnershipHistoryAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'assigned_at', 'assigned_by')
    list_filter = ('assigned_at', 'user', 'assigned_by')  # Enables filtering by date and user
    search_fields = ('task__title', 'user__username', 'assigned_by__username')  # Search by task title, user, and assigned_by usernames
    ordering = ('-assigned_at',)  # Order by the latest assignments first

    def get_readonly_fields(self, request, obj=None):
        # Make all fields read-only in the admin interface
        return [f.name for f in self.model._meta.fields]

# Contribution Admin
@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'rating','rating_summary','submitted_at')
    search_fields = ('user__username', 'task__title')
    readonly_fields = ('submitted_at',)
