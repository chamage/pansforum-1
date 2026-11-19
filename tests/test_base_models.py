import ast
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.accounts.models import Profile
from apps.categories.models import Category
from apps.comments.models import Comment
from apps.moderation.models import Report
from apps.posts.models import Post
from apps.votes.models import Vote

User = get_user_model()


class BaseModelsAndConstraintsTests(TestCase):
    """Verify ETAP 0 base models and PostgreSQL database constraints."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="student1", password="secret-password-123")
        self.other_user = User.objects.create_user(username="student2", password="secret-password-123")
        self.profile = Profile.objects.create(user=self.user, role=Profile.Role.USER)
        self.category = Category.objects.create(name="Ogłoszenia", slug="ogloszenia")
        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title="Przykładowy post",
            body="Treść przykładowego posta.",
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.other_user,
            body="Przykładowy komentarz.",
        )

    def test_valid_vote_and_report_creation(self) -> None:
        post_vote = Vote.objects.create(user=self.user, post=self.post, value=Vote.Value.UP)
        comment_vote = Vote.objects.create(user=self.user, comment=self.comment, value=Vote.Value.DOWN)
        post_report = Report.objects.create(
            reporter=self.other_user,
            post=self.post,
            reason="Spam",
        )
        comment_report = Report.objects.create(
            reporter=self.user,
            comment=self.comment,
            reason="Naruszenie regulaminu",
        )

        self.assertEqual(self.profile.role, Profile.Role.USER)
        self.assertEqual(post_vote.value, 1)
        self.assertEqual(comment_vote.value, -1)
        self.assertEqual(post_report.status, Report.Status.PENDING)
        self.assertEqual(comment_report.status, Report.Status.PENDING)

    def test_vote_rejects_missing_or_both_targets_in_db(self) -> None:
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(user=self.user, value=Vote.Value.UP)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(
                    user=self.user,
                    post=self.post,
                    comment=self.comment,
                    value=Vote.Value.UP,
                )

    def test_vote_rejects_invalid_value_in_db_and_clean(self) -> None:
        for bad_value in (0, 2):
            with self.assertRaises(IntegrityError):
                with transaction.atomic():
                    Vote.objects.create(user=self.user, post=self.post, value=bad_value)

            invalid_vote = Vote(user=self.user, post=self.post, value=bad_value)
            with self.assertRaises(ValidationError):
                invalid_vote.clean()

    def test_vote_rejects_duplicate_user_target(self) -> None:
        Vote.objects.create(user=self.user, post=self.post, value=Vote.Value.UP)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(user=self.user, post=self.post, value=Vote.Value.DOWN)

        Vote.objects.create(user=self.user, comment=self.comment, value=Vote.Value.UP)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(user=self.user, comment=self.comment, value=Vote.Value.DOWN)

    def test_report_rejects_missing_or_both_targets_in_db_and_clean(self) -> None:
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Report.objects.create(reporter=self.user, reason="Brak celu")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Report.objects.create(
                    reporter=self.user,
                    post=self.post,
                    comment=self.comment,
                    reason="Oba cele",
                )

        bad_report = Report(reporter=self.user, reason="Brak celu")
        with self.assertRaises(ValidationError):
            bad_report.clean()

    def test_production_code_does_not_import_test_fakes(self) -> None:
        base_dir = Path(settings.BASE_DIR)
        for root_name in ("core", "apps", "config"):
            for py_file in (base_dir / root_name).rglob("*.py"):
                if "tests" in py_file.parts or "migrations" in py_file.parts:
                    continue
                tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertFalse(
                                alias.name == "tests" or alias.name.startswith("tests."),
                                f"{py_file} must not import {alias.name}",
                            )
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        self.assertFalse(
                            node.module == "tests" or node.module.startswith("tests."),
                            f"{py_file} must not import from {node.module}",
                        )
