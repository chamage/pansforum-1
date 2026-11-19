from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Vote(models.Model):
    """Single user vote (+1 or -1) on either a post or a comment (never both)."""

    class Value(models.IntegerChoices):
        UP = 1, "+1"
        DOWN = -1, "-1"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="votes",
    )
    comment = models.ForeignKey(
        "comments.Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="votes",
    )
    value = models.SmallIntegerField(choices=Value.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(value__in=[1, -1]),
                name="vote_value_is_plus_or_minus_one",
            ),
            models.CheckConstraint(
                condition=(
                    (Q(post__isnull=False) & Q(comment__isnull=True))
                    | (Q(post__isnull=True) & Q(comment__isnull=False))
                ),
                name="vote_exactly_one_target",
            ),
            models.UniqueConstraint(
                fields=["user", "post"],
                condition=Q(post__isnull=False),
                name="vote_unique_user_post",
            ),
            models.UniqueConstraint(
                fields=["user", "comment"],
                condition=Q(comment__isnull=False),
                name="vote_unique_user_comment",
            ),
        ]

    def clean(self) -> None:
        if self.value not in (self.Value.UP, self.Value.DOWN):
            raise ValidationError("Wartość głosu musi wynosić +1 lub -1.")
        if bool(self.post_id) == bool(self.comment_id):
            raise ValidationError("Głos musi wskazywać dokładnie jeden cel: post albo komentarz.")

    def __str__(self) -> str:
        target = f"post #{self.post_id}" if self.post_id else f"comment #{self.comment_id}"
        return f"Vote {self.value:+d} by {self.user} on {target}"
