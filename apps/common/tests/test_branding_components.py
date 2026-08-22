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

    def test_zoomable_media_exposes_an_accessible_dialog(self):
        image = SimpleNamespace(
            url="/media/catalog/products/chaqueta.webp",
            width=1200,
            height=900,
        )

        html = render_to_string(
            "components/ui/zoomable_media.html",
            {
                "image": image,
                "alt": "Chaqueta negra",
                "dialog_id": "product-image-dialog",
            },
        )

        self.assertIn('aria-haspopup="dialog"', html)
        self.assertIn('aria-controls="product-image-dialog"', html)
        self.assertIn('id="product-image-dialog"', html)
        self.assertIn('aria-label="Vista ampliada de Chaqueta negra"', html)
        self.assertIn('data-image-zoom-close', html)

    def test_zoomable_media_does_not_open_dialog_for_fallback_icon(self):
        html = render_to_string(
            "components/ui/zoomable_media.html",
            {
                "image": None,
                "alt": "Sin imagen",
                "dialog_id": "fallback-dialog",
            },
        )

        self.assertNotIn('data-image-zoom-trigger', html)
        self.assertNotIn('data-image-zoom-dialog', html)
        self.assertIn("assets/branding/icon.svg", html)

    def test_zoomable_media_supports_compact_and_hero_variants(self):
        image = SimpleNamespace(
            url="/media/site/hero.webp",
            width=1600,
            height=1200,
        )

        compact_html = render_to_string(
            "components/ui/zoomable_media.html",
            {
                "image": image,
                "alt": "Colección de chaquetas",
                "dialog_id": "compact-image-dialog",
                "compact": True,
            },
        )
        hero_html = render_to_string(
            "components/ui/zoomable_media.html",
            {
                "image": image,
                "alt": "Chaquetas y buzos hechos para ti",
                "dialog_id": "home-hero-image-dialog",
                "hero": True,
            },
        )

        self.assertIn("h-10 w-10", compact_html)
        self.assertIn('<span class="sr-only">Ampliar</span>', compact_html)
        self.assertIn("aspect-video lg:aspect-4/3", hero_html)
        self.assertIn('aria-controls="home-hero-image-dialog"', hero_html)

    def test_zoomable_media_renders_responsive_sources_and_keeps_original_zoom(self):
        original = SimpleNamespace(
            url="/media/content/original.webp",
            width=1800,
            height=1200,
        )
        small = SimpleNamespace(
            url="/media/CACHE/images/small.webp",
            width=320,
            height=240,
        )
        display = SimpleNamespace(
            url="/media/CACHE/images/card.webp",
            width=640,
            height=480,
        )
        desktop = SimpleNamespace(
            url="/media/CACHE/images/desktop.webp",
            width=1200,
            height=900,
        )

        html = render_to_string(
            "components/ui/zoomable_media.html",
            {
                "image": original,
                "display_image": display,
                "small_image": small,
                "desktop_image": desktop,
                "alt": "Chaquetas y buzos",
                "dialog_id": "responsive-image-dialog",
            },
        )

        self.assertIn('<source media="(min-width: 1024px)"', html)
        self.assertIn("/media/CACHE/images/desktop.webp", html)
        self.assertIn(
            'srcset="/media/CACHE/images/small.webp 320w, '
            '/media/CACHE/images/card.webp 640w"',
            html,
        )
        self.assertIn('src="/media/CACHE/images/card.webp"', html)
        self.assertIn('src="/media/content/original.webp"', html)

    def test_public_cards_create_unique_zoom_dialogs(self):
        image = SimpleNamespace(
            url="/media/content/image.webp",
            width=1200,
            height=900,
        )
        business = SimpleNamespace(
            name="Confecciones",
            slug="confecciones",
            image=image,
            short_description="Prendas para ti.",
        )
        cases = (
            (
                "components/cards/product_card.html",
                {
                    "product": SimpleNamespace(
                        business=business,
                        name="Chaquetas",
                        slug="chaquetas",
                        image=image,
                        short_description="Chaquetas cómodas.",
                        show_price=False,
                        price=None,
                    )
                },
                "product-card-image-confecciones-chaquetas",
            ),
            (
                "components/cards/project_card.html",
                {
                    "project": SimpleNamespace(
                        business=business,
                        title="Colección inicial",
                        slug="coleccion-inicial",
                        image=image,
                        short_description="Proyecto de confección.",
                        client_name="Pámi",
                    )
                },
                "project-card-image-confecciones-coleccion-inicial",
            ),
            (
                "components/cards/post_card.html",
                {
                    "post": SimpleNamespace(
                        business=business,
                        title="Ideas para combinar",
                        slug="ideas-para-combinar",
                        image=image,
                        excerpt="Consejos para tu estilo.",
                        published_at=None,
                    )
                },
                "post-card-image-ideas-para-combinar",
            ),
            (
                "components/cards/business_card.html",
                {"business": business},
                "business-card-image-confecciones",
            ),
        )

        for template_name, context, dialog_id in cases:
            with self.subTest(template=template_name):
                html = render_to_string(template_name, context)
                self.assertIn(f'aria-controls="{dialog_id}"', html)
                self.assertIn(f'id="{dialog_id}"', html)
