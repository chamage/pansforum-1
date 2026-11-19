"""Shared views and UI style preview (ETAP 0).

Important: /ui-preview/ uses static demonstration data only and must never import
module models or test fakes.
"""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Temporary home feed with demo data; M3 will replace this source with Post queries.

    The demonstration is deliberately disabled when DEBUG=False until M3 is ready.
    """ 
    if not settings.DEBUG:
        raise Http404("The real feed will be enabled when module M3 is integrated.")

    demo_categories = [
        {"name": "Wszystko", "slug": "wszystkie", "active": True},
        {"name": "Ogłoszenia", "slug": "ogloszenia", "active": False},
        {"name": "Przedmioty i sesja", "slug": "przedmioty-i-sesja", "active": False},
        {"name": "Sprawy studenckie", "slug": "sprawy-studenckie", "active": False},
        {"name": "Koła naukowe", "slug": "kola-naukowe", "active": False},
    ]

    demo_posts = [
        {
            "id": 1,
            "category": "Przedmioty i sesja",
            "author": "anna.kowalska",
            "created_at_display": "2 godz. temu",
            "age_days": 0,
            "title": "Termin oddania projektu z Podstaw Programowania",
            "body": (
                "Cześć! Czy prowadzący potwierdził na ostatnim wykładzie, że repozytorium "
                "z etapem zerowym trzeba wysłać do piątku do 23:59, czy termin został "
                "przesunięty na poniedziałek?"
            ),
            "score": 14,
            "user_vote": 1,
            "comments_count": 2,
        },
        {
            "id": 2,
            "category": "Sprawy studenckie",
            "author": "marek.nowak",
            "created_at_display": "wczoraj",
            "age_days": 1,
            "title": "Godziny otwarcia czytelni przed sesją zimową",
            "body": (
                "Od przyszłego poniedziałku czytelnia główna ma być czynna dłużej — do 19:30 "
                "w dni robocze. Dobrze zabrać legitymację przy wejściu po 16:00."
            ),
            "score": 7,
            "user_vote": 0,
            "comments_count": 0,
        },
    ]

    demo_posts.append({
        "id": 3,
        "category": "Ogłoszenia",
        "author": "piotr.zielinski",
        "created_at_display": "3 dni temu",
        "age_days": 3,
        "title": "Materiały z ćwiczeń dostępne w bibliotece",
        "body": "Dodałem zestaw przykładów z ostatnich zajęć. Można je znaleźć w czytelni.",
        "score": 23,
        "user_vote": 0,
        "comments_count": 5,
    })

    top_periods = [
        {"slug": "today", "label": "Dzisiaj", "max_days": 0},
        {"slug": "week", "label": "W tym tygodniu", "max_days": 7},
        {"slug": "month", "label": "W tym miesiącu", "max_days": 30},
        {"slug": "semester", "label": "W tym semestrze", "max_days": 150},
        {"slug": "all", "label": "Od początku", "max_days": None},
    ]
    period_by_slug = {period["slug"]: period for period in top_periods}

    raw_category = request.GET.get("category", "wszystkie")
    selected_category = next(
        (cat for cat in demo_categories if cat["slug"] == raw_category),
        demo_categories[0],
    )
    raw_sort = request.GET.get("sort", "recent")
    selected_sort = raw_sort if raw_sort in ("recent", "top") else "recent"
    raw_period = request.GET.get("t", "all")
    selected_period = raw_period if raw_period in period_by_slug else "all"
    search_query = request.GET.get("q", "").strip()[:100]
    show_search = request.GET.get("search") == "1" or bool(search_query)

    for category in demo_categories:
        category["active"] = category["slug"] == selected_category["slug"]

    if selected_category["slug"] != "wszystkie":
        demo_posts = [
            post for post in demo_posts if post["category"] == selected_category["name"]
        ]
    if search_query:
        query = search_query.casefold()
        demo_posts = [
            post for post in demo_posts
            if query in post["title"].casefold() or query in post["body"].casefold()
        ]
    if selected_sort == "top":
        max_days = period_by_slug[selected_period]["max_days"]
        if max_days is not None:
            demo_posts = [post for post in demo_posts if post["age_days"] <= max_days]
        demo_posts.sort(key=lambda post: post["score"], reverse=True)

    demo_comments = [
        {
            "id": 101,
            "author": "piotr.zielinski",
            "created_at_display": "1 godz. temu",
            "body": (
                "Na ćwiczeniach mówił, że piątek 23:59 zostaje bez zmian dla etapu 0, "
                "a kolejne moduły sprawdzamy dopiero za dwa tygodnie."
            ),
            "score": 5,
            "user_vote": 1,
        },
        {
            "id": 102,
            "author": "kasia.wisniewska",
            "created_at_display": "42 min temu",
            "body": "Potwierdzam, wpis w sylabusie też ma datę piątkową.",
            "score": 2,
            "user_vote": 0,
        },
    ]

    context = {
        "demo_categories": demo_categories,
        "demo_posts": demo_posts,
        "demo_comments": demo_comments,
        "preview_mode": True,
        "selected_category": selected_category,
        "selected_sort": selected_sort,
        "selected_period": selected_period,
        "selected_period_label": period_by_slug[selected_period]["label"],
        "top_periods": top_periods,
        "search_query": search_query,
        "show_search": show_search,
    }
    return render(request, "core/ui_preview.html", context)


def ui_preview(request: HttpRequest) -> HttpResponse:
    """Backward-compatible URL for the UI preview; / is the canonical dev feed."""
    if not settings.DEBUG:
        raise Http404("UI preview is only available when DEBUG=True.")
    return home(request)


def ui_components(request: HttpRequest) -> HttpResponse:
    """Render the separate UI component gallery (development only)."""
    if not settings.DEBUG:
        raise Http404("UI components are only available when DEBUG=True.")
    # Reuse the static preview data without introducing dependencies on M1-M6.
    # The gallery only needs the comment examples from the reference context.
    context = {"preview_mode": True, "demo_comments": [
        {"author": "piotr.zielinski", "created_at_display": "1 godz. temu",
         "body": "Dzięki, to rozwiązuje problem.", "score": 5, "user_vote": 1},
        {"author": "kasia.wisniewska", "created_at_display": "42 min temu",
         "body": "Potwierdzam.", "score": 2, "user_vote": 0},
    ]}
    return render(request, "core/ui_components.html", context)
