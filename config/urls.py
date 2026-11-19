"""Root URL configuration for PANS Forum."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Tymczasowe / z danymi demonstracyjnymi; M3 podłączy prawdziwe posty.
    path("", include("core.urls")),
    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("categories/", include(("apps.categories.urls", "categories"), namespace="categories")),
    path("posts/", include(("apps.posts.urls", "posts"), namespace="posts")),
    path("comments/", include(("apps.comments.urls", "comments"), namespace="comments")),
    path("votes/", include(("apps.votes.urls", "votes"), namespace="votes")),
    path("moderation/", include(("apps.moderation.urls", "moderation"), namespace="moderation")),
]
