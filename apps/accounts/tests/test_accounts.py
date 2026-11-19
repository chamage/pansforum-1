from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import Profile
from apps.accounts.services import DjangoAccessChecker
from core.contracts import ContentRef, PostRef

User = get_user_model()


class AccountIntegrationTests(TestCase):
    def test_registration_creates_student_profile_and_session(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "student1",
            "email": "student@example.com",
            "password1": "safe-Test-Pass-123",
            "password2": "safe-Test-Pass-123",
        })
        self.assertRedirects(response, reverse("accounts:profile"))
        user = User.objects.get(username="student1")
        self.assertEqual(user.profile.role, Profile.Role.USER)
        self.assertEqual(user.email, "student@example.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_invalid_registration_does_not_create_user(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "student1",
            "password1": "safe-Test-Pass-123",
            "password2": "mismatch",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="student1").exists())

    def test_login_and_post_only_logout(self):
        User.objects.create_user(username="ola", password="safe-Test-Pass-123")
        response = self.client.post(reverse("accounts:login"), {
            "username": "ola",
            "password": "safe-Test-Pass-123",
        })
        self.assertRedirects(response, reverse("accounts:profile"))
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("accounts:logout")), reverse("accounts:login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_profile_requires_login_and_can_be_edited(self):
        self.assertRedirects(
            self.client.get(reverse("accounts:profile")),
            f"{reverse('accounts:login')}?next={reverse('accounts:profile')}",
        )
        user = User.objects.create_user(username="ola", password="safe-Test-Pass-123")
        self.client.force_login(user)
        response = self.client.post(reverse("accounts:profile"), {
            "first_name": "Ola",
            "last_name": "Nowak",
            "email": "ola@example.com",
            "bio": "Matematyka",
        })
        self.assertRedirects(response, reverse("accounts:profile"))
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Ola")
        self.assertEqual(user.profile.bio, "Matematyka")
        self.assertContains(self.client.get(reverse("accounts:profile")), "Student")


class AccessCheckerTests(TestCase):
    def setUp(self):
        self.checker = DjangoAccessChecker()
        self.student = User.objects.create_user(username="student")
        self.moderator = User.objects.create_user(username="moderator")
        self.admin = User.objects.create_user(username="administrator")
        self.staff = User.objects.create_user(username="staff", is_staff=True)
        self.superuser = User.objects.create_superuser(username="root", email="root@example.com", password="Root-Pass-123")
        Profile.objects.create(user=self.student, role=Profile.Role.USER)
        Profile.objects.create(user=self.moderator, role=Profile.Role.MODERATOR)
        Profile.objects.create(user=self.admin, role=Profile.Role.ADMIN)
        Profile.objects.create(user=self.staff, role=Profile.Role.USER)

    def test_role_hierarchy(self):
        self.assertTrue(self.checker.has_role(self.student.pk, "user"))
        self.assertFalse(self.checker.has_role(self.student.pk, "moderator"))
        self.assertTrue(self.checker.has_role(self.moderator.pk, "moderator"))
        self.assertFalse(self.checker.has_role(self.moderator.pk, "admin"))
        self.assertTrue(self.checker.has_role(self.admin.pk, "moderator"))
        self.assertTrue(self.checker.has_role(self.admin.pk, "admin"))

    def test_staff_is_not_forum_moderator_and_superuser_is_admin(self):
        self.assertFalse(self.checker.has_role(self.staff.pk, "moderator"))
        self.assertTrue(self.checker.has_role(self.superuser.pk, "admin"))

    def test_inactive_unknown_and_anonymous_users_are_denied(self):
        self.student.is_active = False
        self.student.save()
        self.assertFalse(self.checker.has_role(self.student.pk, "user"))
        self.assertFalse(self.checker.has_role(999999, "user"))
        self.assertFalse(self.checker.has_role(None, "user"))

    def test_authorship_uses_author_id_and_active_user(self):
        post = PostRef(id=1, author_id=self.student.pk, category_id=2)
        comment = ContentRef(kind="comment", id=3, author_id=self.moderator.pk)
        self.assertTrue(self.checker.is_author(self.student.pk, post))
        self.assertTrue(self.checker.is_author(self.moderator.pk, comment))
        self.assertFalse(self.checker.is_author(self.student.pk, comment))
        self.assertFalse(self.checker.is_author(None, post))
