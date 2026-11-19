"""Shared data references and module boundary contracts for PANS Forum.

Frozen at ETAP 0 so modules M1-M6 can develop and test against stable interfaces.
Changes to names or semantics require agreement across dependent modules.
"""

from dataclasses import dataclass
from typing import Literal, Protocol

ContentKind = Literal["post", "comment"]
RoleName = Literal["user", "moderator", "admin"]


@dataclass(frozen=True, slots=True)
class PostRef:
    """Minimal post reference exposed across module boundaries."""

    id: int
    author_id: int
    category_id: int
    hidden: bool = False


@dataclass(frozen=True, slots=True)
class ContentRef:
    """Minimal reference to a votable or reportable target (post or comment)."""

    kind: ContentKind
    id: int
    author_id: int
    hidden: bool = False


class CategoryCatalog(Protocol):
    """Contract consumed by M3 (posts) and provided by M2 (categories)."""

    def category_exists(self, category_id: int) -> bool:
        """Return True if the category exists, False otherwise."""
        ...


class PostReader(Protocol):
    """Contract consumed by M4 (comments) and provided by M3 (posts)."""

    def get_post(self, post_id: int) -> PostRef | None:
        """Return PostRef if the post exists and is public, None otherwise."""
        ...


class ContentLookup(Protocol):
    """Contract consumed by M5 (votes) and M6 (moderation), provided by M3/M4."""

    def get_target(self, kind: ContentKind, id: int) -> ContentRef | None:
        """Return ContentRef for a post or comment, or None if missing."""
        ...


class AccessChecker(Protocol):
    """Contract consumed by M3-M6 and provided by M1 (accounts)."""

    def is_author(self, user_id: int | None, target: PostRef | ContentRef) -> bool:
        """Return True only when user_id matches the target's author_id."""
        ...

    def has_role(self, user_id: int | None, role: RoleName) -> bool:
        """Return True only when the user exists and holds the given role."""
        ...


class ContentModeration(Protocol):
    """Contract consumed by M6 (moderation) and provided by M3/M4."""

    def hide_content(self, kind: ContentKind, id: int) -> bool:
        """Hide a post or comment without physical deletion; return True on success."""
        ...
