from django.apps import AppConfig


class TeamtasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teamtasks'

    def ready(self):
        import teamtasks.signals  # Ensure the signal is loaded