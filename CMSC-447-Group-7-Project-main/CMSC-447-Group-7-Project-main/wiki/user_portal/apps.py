from django.apps import AppConfig


class UserPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_portal'

    def ready(self):
        # Import signals and connect them when the app is fully loaded
        from django.db.models.signals import post_migrate
        from user_portal.signals import create_roles_and_permissions
        
        post_migrate.connect(create_roles_and_permissions)
