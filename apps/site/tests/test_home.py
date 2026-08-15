from django.test import TestCase
from django.urls import reverse

from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.portfolio.models import PortfolioProject
from apps.site.models import SiteConfiguration


class HomeViewTests(TestCase):
    def setUp(self):
        self.public_business = Business.objects.create(
            name="Confecciones",
            slug="confecciones",
            is_active=True,
            is_published=True,
        )
        SiteConfiguration.objects.create(
            featured_business=self.public_business,
        )
        self.hidden_business = Business.objects.create(
            name="Tecnología",
            slug="tecnologia",
            is_active=True,
            is_published=True,
        )

    def test_home_only_contains_published_confections_content(self):
        jacket = Product.objects.create(
            business=self.public_business,
            name="Chaquetas",
            slug="chaquetas",
            order=1,
            is_active=True,
            is_published=True,
        )
        sweatshirt = Product.objects.create(
            business=self.public_business,
            name="Buzos",
            slug="buzos",
            order=2,
            is_active=True,
            is_published=True,
        )
        Product.objects.create(
            business=self.public_business,
            name="Producto adicional",
            slug="producto-adicional",
            order=3,
            is_active=True,
            is_published=True,
        )
        Product.objects.create(
            business=self.hidden_business,
            name="Producto de otra línea",
            slug="producto-otra-linea",
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
            business=self.hidden_business,
            title="Proyecto de otra línea",
            slug="proyecto-otra-linea",
            is_active=True,
            is_published=True,
        )

        response = self.client.get(reverse("site:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["business"], self.public_business)
        self.assertQuerySetEqual(response.context["products"], [jacket, sweatshirt])
        self.assertQuerySetEqual(response.context["projects"], [public_project])
        self.assertNotIn("businesses", response.context)
        self.assertNotIn("posts", response.context)
        self.assertContains(response, "Nuestras confecciones")
        self.assertNotContains(response, "Producto de otra línea")
        self.assertContains(response, "Donde encuentras todo para ti")
        self.assertContains(response, "Confecciones")

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

    def test_home_keeps_its_query_budget(self):
        Product.objects.create(
            business=self.public_business,
            name="Chaquetas",
            slug="chaquetas",
            is_active=True,
            is_published=True,
        )
        PortfolioProject.objects.create(
            business=self.public_business,
            title="Colección inicial",
            slug="coleccion-inicial",
            is_active=True,
            is_published=True,
        )

        with self.assertNumQueries(5):
            response = self.client.get(reverse("site:home"))

        self.assertEqual(response.status_code, 200)
