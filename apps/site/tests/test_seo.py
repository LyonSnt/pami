from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product


class SeoTests(TestCase):
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
