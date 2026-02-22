from django.apps import AppConfig

class SleekappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sleekApp'

    def ready(self):
        import sleekApp.signals