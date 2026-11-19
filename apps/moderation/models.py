from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Report(models.Model):
    """User report flagging either a post or a comment for moderator review."""

    class Status(models.TextChoices):
        PENDING = "pending", "Oczekujące"
        DISMISSED = "dismissed", "Odrzucone"
        RESOLVED = "resolved", "Ukryto treść"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_submitted",
    )
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports",
    )
    comment = models.ForeignKey(
        "comments.Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports",
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_reviewed",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    (Q(post__isnull=False) & Q(comment__isnull=True))
                    | (Q(post__isnull=True) & Q(comment__isnull=False))
                ),
                name="report_exactly_one_target",
            ),
        ]

    def clean(self) -> None:
        if bool(self.post_id) == bool(self.comment_id):
            raise ValidationError(
                "Zgłoszenie musi wskazywać dokładnie jeden cel: post albo komentarz."
            )

    def __str__(self) -> str:
        target = f"post #{self.post_id}" if self.post_id else f"comment #{self.comment_id}"
        return f"Report #{self.pk} ({self.status}) on {target}"
