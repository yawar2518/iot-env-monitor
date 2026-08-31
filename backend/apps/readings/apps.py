from django.apps import AppConfig


class ReadingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.readings'
    verbose_name = 'Readings'

    def ready(self):
        pass  # Signal handlers will be imported here in M3