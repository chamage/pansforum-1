from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the shared core app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
