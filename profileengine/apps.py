from django.apps import AppConfig


class ProfileengineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profileengine'

    def ready(self):
        import profileengine.signals
