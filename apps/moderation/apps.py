from django.apps import AppConfig


class ModerationConfig(AppConfig):
    """Configuration for M6: moderation and reports."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.moderation"
    label = "moderation"
