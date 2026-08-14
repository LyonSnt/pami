from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import SimpleTestCase


class BrandingAssetTests(SimpleTestCase):
    def test_required_branding_assets_exist(self):
        for asset in (
            "assets/branding/logo.svg",
            "assets/branding/logo-white.svg",
            "assets/branding/icon.svg",
            "assets/branding/favicon.svg",
        ):
            with self.subTest(asset=asset):
                self.assertIsNotNone(finders.find(asset))

    def test_card_media_uses_decorative_brand_fallback(self):
        html = render_to_string(
            "components/ui/card_media.html",
            {"image": None, "alt": "Contenido"},
        )

        self.assertIn("assets/branding/icon.svg", html)
        self.assertIn('alt=""', html)
        self.assertIn('aria-hidden="true"', html)
