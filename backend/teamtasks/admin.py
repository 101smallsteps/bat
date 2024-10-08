from django.contrib import admin
from .models import Project, Job, StaffApplication, UserDetails, Task, TaskComment, Contribution

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
    list_display = ('title', 'project')
    list_filter = ('project',)
    search_fields = ('title', 'description', 'responsibilities')
    filter_horizontal = ('prerequisites',)  # Allows for multi-selection for many-to-many fields

# Staff Application Admin
@admin.register(StaffApplication)
class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution_name', 'job', 'approved', 'generated_at', 'approved_at')
    list_filter = ('approved', 'institution_state', 'generated_at')
    search_fields = ('user__username', 'institution_name', 'job__title', 'email', 'phone')
    readonly_fields = ('confirmation_id', 'generated_at', 'approved_at')

# User Details Admin
@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol')
    search_fields = ('user__username',)
    readonly_fields = ('user',)  # Useful if user should not change once set

# Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'priority', 'task_type', 'completed', 'created_at', 'completed_at')
    list_filter = ('priority', 'task_type', 'completed')
    search_fields = ('title', 'description', 'assigned_to__username')
    autocomplete_fields = ('previous_task',)  # Allows easier selection of related tasks

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
