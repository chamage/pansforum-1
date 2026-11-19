from django.test import SimpleTestCase, override_settings


class UiPreviewSmokeTests(SimpleTestCase):
    """UI feed preview and separate component gallery are development-only."""

    @override_settings(DEBUG=True)
    def test_feed_preview_renders_realistic_feed_without_debug_copy(self):
        response = self.client.get("/ui-preview/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "core/ui_preview.html")
        self.assertTemplateUsed(response, "partials/post_card.html")
        content = response.content.decode("utf-8")
        self.assertIn("Termin oddania projektu z Podstaw Programowania", content)
        self.assertIn("Napisz post…", content)
        self.assertNotIn("Wzorzec interfejsu", content)
        self.assertNotIn("Tryb podglądu", content)
        self.assertNotIn("site-footer", content)

    @override_settings(DEBUG=True)
    def test_home_category_sort_search_and_empty_state(self):
        home = self.client.get("/")
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "Wszystko")
        self.assertContains(home, 'id="category-filter-input"')
        self.assertContains(home, "Najnowsze")
        self.assertContains(home, "Najwyżej oceniane")
        self.assertContains(home, "Dzisiaj")
        self.assertContains(home, "W tym tygodniu")
        self.assertContains(home, "W tym miesiącu")
        self.assertContains(home, "W tym semestrze")
        self.assertContains(home, "Od początku")
        self.assertContains(home, "post-meta__category")
        self.assertNotContains(home, "feed-status")
        self.assertNotContains(home, "feed-sort__trigger--active")
        self.assertNotContains(home, "feed-sort__top-icon")
        self.assertNotContains(home, 'aria-label="Nowy post')

        category = self.client.get("/?category=sprawy-studenckie")
        self.assertContains(category, "Godziny otwarcia czytelni")
        self.assertNotContains(category, "Termin oddania projektu")

        top = self.client.get("/?sort=top")
        self.assertContains(top, "feed-sort__trigger--active")
        self.assertContains(top, "feed-sort__top-icon")
        self.assertNotContains(top, "feed-sort__dot")
        self.assertContains(top, '<span class="feed-sort__label">Od początku</span>')
        page = top.content.decode("utf-8")
        self.assertLess(
            page.find("Materiały z ćwiczeń dostępne"),
            page.find("Termin oddania projektu"),
        )

        top_today = self.client.get("/?sort=top&t=today")
        self.assertContains(top_today, '<span class="feed-sort__label">Dzisiaj</span>')
        self.assertContains(top_today, "Termin oddania projektu")
        self.assertNotContains(top_today, "Materiały z ćwiczeń dostępne")

        search = self.client.get("/?search=1&q=czytelni")
        self.assertContains(search, "Szukaj postów")
        self.assertContains(search, "Godziny otwarcia czytelni")
        self.assertNotContains(search, "Termin oddania projektu")

        empty = self.client.get("/?category=kola-naukowe")
        self.assertContains(empty, "Brak postów")

    @override_settings(DEBUG=True)
    def test_components_gallery_contains_fields_and_comments(self):
        response = self.client.get("/ui-components/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/ui_components.html")
        self.assertTemplateUsed(response, "partials/comment_item.html")
        content = response.content.decode("utf-8")
        self.assertIn('for="preview-username"', content)
        self.assertIn('for="preview-password"', content)
        self.assertIn("Brak postów", content)

    @override_settings(DEBUG=False)
    def test_developer_preview_pages_return_404_in_production(self):
        for url in ("/", "/ui-preview/", "/ui-components/"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
