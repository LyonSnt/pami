from types import SimpleNamespace
from xml.etree import ElementTree

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

    def test_logo_name_uses_contiguous_colored_segments(self):
        logo_path = finders.find("assets/branding/logo.svg")
        root = ElementTree.parse(logo_path).getroot()
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        wordmark = root.find("svg:text[@x='56']", namespace)
        segments = wordmark.findall("svg:tspan", namespace)

        self.assertEqual([segment.text for segment in segments], ["Pá", "mi"])
        self.assertEqual(
            [segment.attrib["fill"] for segment in segments],
            ["#E31B23", "#0D1117"],
        )
        self.assertIsNone(segments[0].tail)

    def test_card_media_uses_decorative_brand_fallback(self):
        html = render_to_string(
            "components/ui/card_media.html",
            {"image": None, "alt": "Contenido"},
        )

        self.assertIn("assets/branding/icon.svg", html)
        self.assertIn('alt=""', html)
        self.assertIn('aria-hidden="true"', html)

    def test_footer_renders_configured_slogan(self):
        html = render_to_string(
            "base/_footer.html",
            {
                "site_configuration": SimpleNamespace(
                    site_name="Pámi",
                    slogan="Donde encuentras todo para ti",
                    email="",
                    phone="",
                    address="",
                ),
            },
        )

        self.assertIn("Donde encuentras todo para ti", html)
