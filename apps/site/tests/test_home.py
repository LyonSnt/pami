from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.portfolio.models import PortfolioProject
from apps.site.models import SiteConfiguration


class HomeViewTests(TestCase):
    def setUp(self):
        SiteConfiguration.objects.create()
        self.public_business = Business.objects.create(
            name="Negocio público",
            slug="negocio-publico",
            is_active=True,
            is_published=True,
        )
        self.hidden_business = Business.objects.create(
            name="Negocio oculto",
            slug="negocio-oculto",
            is_active=False,
            is_published=True,
        )

    def test_home_only_contains_public_content(self):
        public_product = Product.objects.create(
            business=self.public_business,
            name="Producto público",
            slug="producto-publico",
            is_active=True,
            is_published=True,
        )
        Product.objects.create(
            business=self.hidden_business,
            name="Producto oculto",
            slug="producto-oculto",
            is_active=True,
            is_published=True,
        )
        public_project = PortfolioProject.objects.create(
            business=self.public_business,
            title="Proyecto público",
            slug="proyecto-publico",
            is_active=True,
            is_published=True,
        )
        PortfolioProject.objects.create(
            business=self.public_business,
            title="Proyecto oculto",
            slug="proyecto-oculto",
            is_active=False,
            is_published=True,
        )
        public_post = BlogPost.objects.create(
            title="Artículo público",
            slug="articulo-publico",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now(),
        )
        BlogPost.objects.create(
            title="Artículo futuro",
            slug="articulo-futuro",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now() + timedelta(days=1),
        )

        response = self.client.get(reverse("site:home"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["businesses"],
            [self.public_business],
        )
        self.assertQuerySetEqual(response.context["products"], [public_product])
        self.assertQuerySetEqual(response.context["projects"], [public_project])
        self.assertQuerySetEqual(response.context["posts"], [public_post])

    def test_home_contains_global_accessibility_navigation(self):
        response = self.client.get(reverse("site:home"))

        self.assertContains(response, 'href="#main-content"')
        self.assertContains(response, 'id="main-content"')
        self.assertContains(response, "<details", count=1)
        self.assertContains(response, 'aria-label="Navegación principal"', count=2)

    def test_home_uses_branding_and_svg_benefit_icons(self):
        response = self.client.get(reverse("site:home"))

        self.assertContains(response, "assets/branding/favicon.svg")
        self.assertContains(response, "Calidad garantizada")
        self.assertContains(response, "Entrega confiable")
        self.assertContains(response, "Soporte cercano")
        self.assertNotContains(response, ">✓<")
        self.assertNotContains(response, ">◉<")
