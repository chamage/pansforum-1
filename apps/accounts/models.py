from django.conf import settings
from django.db import models


class Profile(models.Model):
    """User profile extending Django's built-in User with a forum role."""

    class Role(models.TextChoices):
        USER = "user", "Użytkownik"
        MODERATOR = "moderator", "Moderator"
        ADMIN = "admin", "Administrator"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    bio = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} ({self.role})"
