from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task, TaskOwnershipHistory
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Task)
def track_task_ownership(sender, instance, **kwargs):
    # Check if the task already exists and if the assigned owner has changed
    if instance.pk:
        previous_task = Task.objects.get(pk=instance.pk)
        if previous_task.assigned_to != instance.assigned_to:
            # Use assigned_by passed through instance to avoid assigning the User class itself
            assigned_by = getattr(instance, '_assigned_by', None)
            if assigned_by and isinstance(assigned_by, User):
                # Record the ownership change in TaskOwnershipHistory
                TaskOwnershipHistory.objects.create(
                    task=instance,
                    user=instance.assigned_to,
                    assigned_by=assigned_by
                )
                print(f"Task ownership updated for {instance} assigned by {assigned_by}")
