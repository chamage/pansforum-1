from django.template.loader import get_template
from django.test import SimpleTestCase
from django.urls import reverse


class UiIntegrationContractTests(SimpleTestCase):
    def test_post_detail_route_is_reserved_for_m3(self):
        self.assertEqual(reverse("posts:post_detail", args=[7]), "/posts/7/")

    def test_integration_templates_exist(self):
        for template_name in (
            "posts/post_detail.html",
            "comments/_list.html",
            "votes/_controls.html",
            "moderation/_report_action.html",
        ):
            with self.subTest(template=template_name):
                self.assertIsNotNone(get_template(template_name))
