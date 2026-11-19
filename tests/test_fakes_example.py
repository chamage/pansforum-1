from django.test import SimpleTestCase

from core.contracts import CategoryCatalog
from tests.fakes import FakeCategoryCatalog


def validate_post_category(category_id: int, catalog: CategoryCatalog) -> int:
    """Example service helper accepting the CategoryCatalog contract."""
    if not catalog.category_exists(category_id):
        raise ValueError(f"Kategoria o id={category_id} nie istnieje.")
    return category_id


class FakeCategoryCatalogExampleTests(SimpleTestCase):
    """Demonstrates unit testing a module dependency with a fake (no DB needed)."""

    def test_fake_category_catalog_returns_true_for_known_id(self) -> None:
        catalog = FakeCategoryCatalog(existing_ids=[1, 4])

        self.assertTrue(catalog.category_exists(1))
        self.assertFalse(catalog.category_exists(999))

    def test_consumer_accepts_existing_category_and_rejects_missing(self) -> None:
        catalog = FakeCategoryCatalog(existing_ids=[10])

        self.assertEqual(validate_post_category(10, catalog), 10)
        with self.assertRaises(ValueError):
            validate_post_category(999, catalog)
