"""Test doubles (fakes) for isolated module unit tests.

Rules:
- Fakes in this module are for automated tests only.
- Production views and services in core/ and apps/ must never import from tests.fakes.
"""

from collections.abc import Iterable


class FakeCategoryCatalog:
    """In-memory fake implementing core.contracts.CategoryCatalog."""

    def __init__(self, existing_ids: Iterable[int]) -> None:
        self._existing_ids = frozenset(existing_ids)

    def category_exists(self, category_id: int) -> bool:
        return category_id in self._existing_ids
