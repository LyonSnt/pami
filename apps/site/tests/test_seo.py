import base64
import json
import re
from datetime import timedelta
from decimal import Decimal
from tempfile import TemporaryDirectory

from django.core.files.base import ContentFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.site.models import SiteConfiguration


class SeoTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media_directory = TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.media_directory.name)
        cls.media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.media_override.disable()
        cls.media_directory.cleanup()

    def setUp(self):
        self.business = Business.objects.create(
            name="Confecciones",
            slug="confecciones",
            short_description="Confecciones para todos los días.",
            is_active=True,
            is_published=True,
        )
        self.product = Product.objects.create(
            business=self.business,
            name="Chaquetas",
            slug="chaquetas",
            short_description="Chaquetas cómodas y versátiles.",
            is_active=True,
            is_published=True,
        )

    def attach_test_image(self, instance, field_name):
        image_content = ContentFile(
            base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
                "AAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
            ),
            name="seo-image.png",
        )
        getattr(instance, field_name).save("seo-image.png", image_content, save=True)

    def get_structured_data(self, response):
        scripts = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            response.content.decode(),
            flags=re.DOTALL,
        )
        return [json.loads(script) for script in scripts]

    def test_public_list_has_primary_heading_and_core_metadata(self):
        response = self.client.get(reverse("catalog:list"))

        self.assertContains(response, "<h1", html=False)
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'rel="canonical" href="http://testserver/catalogo/"')
        self.assertContains(response, 'property="og:title"')
        self.assertContains(response, 'name="twitter:card"')

    def test_success_page_is_not_indexed(self):
        response = self.client.get(reverse("contact:success"))

        self.assertContains(response, 'name="robots" content="noindex, follow"')

    def test_robots_exposes_sitemap_and_private_routes(self):
        response = self.client.get(reverse("robots"))

        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "Disallow: /contacto/enviado/")
        self.assertContains(response, "Sitemap: http://testserver/sitemap.xml")

    def test_sitemap_includes_only_public_current_content(self):
        hidden_product = Product.objects.create(
            business=self.business,
            name="Producto oculto",
            slug="producto-oculto",
            is_active=True,
            is_published=False,
        )
        current_post = BlogPost.objects.create(
            title="Artículo actual",
            slug="articulo-actual",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now(),
        )
        future_post = BlogPost.objects.create(
            title="Artículo futuro",
            slug="articulo-futuro-seo",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now() + timedelta(days=1),
        )

        response = self.client.get(reverse("sitemap"))

        self.assertContains(response, self.product.slug)
        self.assertContains(response, current_post.slug)
        self.assertNotContains(response, hidden_product.slug)
        self.assertNotContains(response, future_post.slug)

    def test_detail_breadcrumbs_expose_full_hierarchy(self):
        post = BlogPost.objects.create(
            title="Ideas para combinar",
            slug="ideas-para-combinar",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now(),
        )

        response = self.client.get(reverse("blog:detail", args=[post.slug]))

        self.assertContains(response, reverse("blog:list"))
        self.assertContains(response, 'aria-current="page"')

    def test_product_uses_specific_social_image_for_open_graph_and_twitter(self):
        self.attach_test_image(self.product, "image")

        response = self.client.get(
            reverse(
                "catalog:detail",
                args=[self.business.slug, self.product.slug],
            )
        )
        expected_url = f"http://testserver{self.product.image.url}"

        self.assertContains(
            response,
            f'property="og:image" content="{expected_url}"',
        )
        self.assertContains(
            response,
            f'name="twitter:image" content="{expected_url}"',
        )
        self.assertContains(
            response,
            'name="twitter:card" content="summary_large_image"',
        )

    def test_organization_structured_data_uses_configured_identity(self):
        SiteConfiguration.objects.create(
            site_name="Pámi",
            description="Confecciones para todos.",
            email="contacto@example.com",
            phone="0999999999",
            instagram_url="https://instagram.com/pami",
        )

        response = self.client.get(reverse("site:home"))
        organization = next(
            data
            for data in self.get_structured_data(response)
            if data["@type"] == "Organization"
        )

        self.assertEqual(organization["name"], "Pámi")
        self.assertEqual(organization["url"], "http://testserver/")
        self.assertEqual(organization["email"], "contacto@example.com")
        self.assertEqual(
            organization["sameAs"],
            ["https://instagram.com/pami"],
        )
        self.assertTrue(organization["logo"].startswith("http://testserver/"))

    def test_product_structured_data_only_includes_visible_price(self):
        self.product.price = Decimal("45.00")
        self.product.show_price = True
        self.product.save(update_fields=["price", "show_price", "updated_at"])

        response = self.client.get(
            reverse(
                "catalog:detail",
                args=[self.business.slug, self.product.slug],
            )
        )
        product_data = next(
            data
            for data in self.get_structured_data(response)
            if data["@type"] == "Product"
        )

        self.assertEqual(product_data["name"], "Chaquetas")
        self.assertEqual(product_data["offers"]["price"], "45.00")
        self.assertEqual(product_data["offers"]["priceCurrency"], "USD")

        self.product.show_price = False
        self.product.save(update_fields=["show_price", "updated_at"])
        response = self.client.get(
            reverse(
                "catalog:detail",
                args=[self.business.slug, self.product.slug],
            )
        )
        product_data = next(
            data
            for data in self.get_structured_data(response)
            if data["@type"] == "Product"
        )
        self.assertNotIn("offers", product_data)

    def test_blog_post_structured_data_contains_publication_information(self):
        post = BlogPost.objects.create(
            business=self.business,
            title="Ideas para combinar",
            slug="ideas-estructuradas",
            excerpt="Consejos para combinar prendas.",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now(),
        )

        response = self.client.get(reverse("blog:detail", args=[post.slug]))
        post_data = next(
            data
            for data in self.get_structured_data(response)
            if data["@type"] == "BlogPosting"
        )

        self.assertEqual(post_data["headline"], post.title)
        self.assertEqual(
            post_data["mainEntityOfPage"],
            f"http://testserver/blog/{post.slug}/",
        )
        self.assertIn("datePublished", post_data)
        self.assertIn("dateModified", post_data)

    def test_structured_data_escapes_script_closing_characters(self):
        self.product.name = "Chaqueta </script><script>alert(1)</script>"
        self.product.save(update_fields=["name", "updated_at"])

        response = self.client.get(
            reverse(
                "catalog:detail",
                args=[self.business.slug, self.product.slug],
            )
        )
        content = response.content.decode()
        product_data = next(
            data
            for data in self.get_structured_data(response)
            if data["@type"] == "Product"
        )

        self.assertNotIn("</script><script>alert(1)</script>", content)
        self.assertIn("\\u003c/script\\u003e", content)
        self.assertEqual(
            product_data["name"],
            "Chaqueta </script><script>alert(1)</script>",
        )
