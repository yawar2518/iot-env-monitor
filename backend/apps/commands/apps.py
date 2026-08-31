from django.apps import AppConfig


class CommandsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.commands'
    verbose_name = 'Commands'

    def ready(self):
        pass  # Signal handlers will be imported here in M5