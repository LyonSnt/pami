from types import SimpleNamespace
from xml.etree import ElementTree

from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import SimpleTestCase

from apps.site.models import SiteConfiguration


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
                    whatsapp_url="",
                    address="",
                    facebook_url="",
                    instagram_url="",
                    tiktok_url="",
                    youtube_url="",
                    linkedin_url="",
                ),
            },
        )

        self.assertIn("Donde encuentras todo para ti", html)

    def test_header_uses_configured_logo(self):
        html = render_to_string(
            "base/_header.html",
            {
                "site_configuration": SimpleNamespace(
                    site_name="Pámi",
                    slogan="",
                    logo=SimpleNamespace(url="/media/site/logo.webp"),
                ),
                "navigation_items": [],
            },
        )

        self.assertIn('src="/media/site/logo.webp"', html)

    def test_footer_renders_contact_links_and_social_networks(self):
        html = render_to_string(
            "base/_footer.html",
            {
                "site_configuration": SimpleNamespace(
                    site_name="Pámi",
                    slogan="",
                    email="contacto@pami.test",
                    phone="099 999 9999",
                    whatsapp_url="https://wa.me/593999999999",
                    address="Ecuador",
                    facebook_url="",
                    instagram_url="https://instagram.com/pami",
                    tiktok_url="",
                    youtube_url="",
                    linkedin_url="",
                ),
            },
        )

        self.assertIn('href="mailto:contacto@pami.test"', html)
        self.assertIn('href="tel:099 999 9999"', html)
        self.assertIn('href="https://wa.me/593999999999"', html)
        self.assertIn('aria-label="Redes sociales"', html)
        self.assertIn('href="https://instagram.com/pami"', html)

    def test_whatsapp_url_keeps_only_digits(self):
        configuration = SiteConfiguration(whatsapp="+593 99 999-9999")

        self.assertEqual(configuration.whatsapp_url, "https://wa.me/593999999999")
