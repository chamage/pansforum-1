"""M1: account creation and the single authorization policy for forum modules."""

from django.contrib.auth import get_user_model
from django.db import transaction

from core.contracts import ContentRef, PostRef, RoleName

from .models import Profile

ROLE_LEVEL = {"user": 0, "moderator": 1, "admin": 2}


class DjangoAccessChecker:
    """Shared AccessChecker implementation for M2-M6.

    Profile.role is authoritative for forum permissions. is_staff only controls
    Django Admin access. A superuser may perform all forum operations.
    """

    def is_author(self, user_id: int | None, target: PostRef | ContentRef) -> bool:
        if user_id is None or target.author_id != user_id:
            return False
        return get_user_model().objects.filter(pk=user_id, is_active=True).exists()

    def has_role(self, user_id: int | None, role: RoleName) -> bool:
        if user_id is None or role not in ROLE_LEVEL:
            return False
        user = get_user_model().objects.filter(pk=user_id, is_active=True).first()
        if user is None:
            return False
        if user.is_superuser:
            return True
        current_role = Profile.objects.filter(user_id=user_id).values_list("role", flat=True).first()
        return ROLE_LEVEL.get(current_role, -1) >= ROLE_LEVEL[role]


@transaction.atomic
def register_account(form):
    """Persist an already validated UserCreationForm and default student profile."""
    user = form.save()
    Profile.objects.create(user=user, role=Profile.Role.USER)
    return user


def get_or_create_profile(user) -> Profile:
    """Keep old Django users and superusers usable without a custom User model."""
    profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": Profile.Role.USER})
    return profile
