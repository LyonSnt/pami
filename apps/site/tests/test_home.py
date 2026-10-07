from django.test import TestCase
from django.urls import reverse

from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.portfolio.models import PortfolioProject
from apps.site.models import SiteConfiguration


class HomeViewTests(TestCase):
    def setUp(self):
        self.public_business = Business.objects.create(
            name="Creaciones Hadasha",
            slug="creaciones",
            is_active=True,
            is_published=True,
        )
        SiteConfiguration.objects.create(
            featured_business=self.public_business,
            hero_label="Creaciones",
        )
        self.hidden_business = Business.objects.create(
            name="Tecnología",
            slug="tecnologia",
            is_active=True,
            is_published=True,
        )

    def test_home_only_contains_published_catalog_content_when_optional_modules_are_off(self):
        jacket = Product.objects.create(
            business=self.public_business,
            name="Chaquetas",
            slug="chaquetas",
            is_featured=True,
            order=1,
            is_active=True,
            is_published=True,
        )
        sweatshirt = Product.objects.create(
            business=self.public_business,
            name="Buzos",
            slug="buzos",
            is_featured=True,
            order=2,
            is_active=True,
            is_published=True,
        )
        Product.objects.create(
            business=self.public_business,
            name="Producto adicional",
            slug="producto-adicional",
            is_featured=True,
            order=3,
            is_active=True,
            is_published=True,
        )
        Product.objects.create(
            business=self.hidden_business,
            name="Producto de otra línea",
            slug="producto-otra-linea",
            is_featured=True,
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
        self.assertEqual(response.context["projects"], [])
        self.assertNotIn("businesses", response.context)
        self.assertNotIn("posts", response.context)
        self.assertContains(response, "Productos y servicios destacados")
        self.assertNotContains(response, public_project.title)
        self.assertNotContains(response, "Producto de otra línea")
        self.assertContains(response, "Donde encuentras todo para ti")
        self.assertContains(response, "Creaciones")
        self.assertContains(response, "Creaciones Hadasha")

    def test_featured_checkbox_controls_home_without_changing_catalog(self):
        first = Product.objects.create(
            business=self.public_business, name="Primero en catálogo", slug="primero", order=1,
        )
        selected = Product.objects.create(
            business=self.public_business, name="Elegido para Home", slug="elegido",
            order=2, is_featured=True,
        )
        response = self.client.get(reverse("site:home"))
        self.assertEqual(list(response.context["products"]), [selected])
        catalog = self.client.get(reverse("catalog:business_list", args=[self.public_business.slug]))
        self.assertEqual(list(catalog.context["products"]), [first, selected])
        selected.is_featured = False
        selected.save()
        self.assertEqual(list(self.client.get(reverse("site:home")).context["products"]), [])
        catalog = self.client.get(reverse("catalog:business_list", args=[self.public_business.slug]))
        self.assertEqual(list(catalog.context["products"]), [first, selected])

    def test_featured_products_still_require_publication_and_activity(self):
        for name, active, published in (("Inactivo", False, True), ("Borrador", True, False)):
            Product.objects.create(
                business=self.public_business, name=name, slug=name.lower(),
                is_featured=True, is_active=active, is_published=published,
            )
        self.assertEqual(list(self.client.get(reverse("site:home")).context["products"]), [])

    def test_home_does_not_fall_back_to_unselected_products(self):
        Product.objects.create(business=self.public_business, name="Solo catálogo", slug="solo-catalogo")
        response = self.client.get(reverse("site:home"))
        self.assertEqual(list(response.context["products"]), [])
        self.assertNotContains(response, "Solo catálogo")

    def test_switching_featured_business_uses_its_selected_products(self):
        stationery = Product.objects.create(
            business=self.hidden_business, name="Agenda destacada", slug="agenda", is_featured=True,
        )
        configuration = SiteConfiguration.objects.get()
        configuration.featured_business = self.hidden_business
        configuration.save()
        self.assertEqual(list(self.client.get(reverse("site:home")).context["products"]), [stationery])

    def test_home_respects_configured_featured_limit(self):
        products = [
            Product.objects.create(
                business=self.public_business, name=f"Destacado {order}",
                slug=f"destacado-{order}", order=order, is_featured=True,
            )
            for order in range(1, 6)
        ]
        configuration = SiteConfiguration.objects.get()
        for limit in (4, 1, 12):
            with self.subTest(limit=limit):
                configuration.featured_products_limit = limit
                configuration.save()
                response = self.client.get(reverse("site:home"))
                self.assertEqual(list(response.context["products"]), products[:limit])

    def test_home_uses_editorial_title_for_any_featured_business(self):
        self.public_business.featured_title = "Prendas destacadas"
        self.public_business.save()
        response = self.client.get(reverse("site:home"))
        self.assertContains(response, "Prendas destacadas")
        self.assertContains(response, "Conoce lo que ofrece Creaciones Hadasha.")
        self.assertNotContains(response, "Productos y servicios destacados")

        self.hidden_business.featured_title = "Sistemas destacados"
        self.hidden_business.save()
        configuration = SiteConfiguration.objects.get()
        configuration.featured_business = self.hidden_business
        configuration.save()
        response = self.client.get(reverse("site:home"))
        self.assertContains(response, "Sistemas destacados")
        self.assertContains(response, "Conoce lo que ofrece Tecnología.")
        self.assertNotContains(response, "Prendas destacadas")

    def test_home_contains_global_accessibility_navigation(self):
        response = self.client.get(reverse("site:home"))

        self.assertContains(response, 'href="#main-content"')
        self.assertContains(response, 'id="main-content"')
        self.assertContains(response, "<details", count=1)
        self.assertContains(response, 'aria-label="Navegación principal"', count=2)
        self.assertContains(response, 'dialog.showModal()')
        self.assertContains(response, 'event.target === dialog')
        self.assertContains(response, 'trigger.focus()')

    def test_home_uses_branding_and_svg_benefit_icons(self):
        response = self.client.get(reverse("site:home"))

        self.assertContains(response, "assets/branding/favicon.svg")
        self.assertContains(response, "Cuidamos los detalles")
        self.assertContains(response, "Entrega confiable")
        self.assertContains(response, "Atención cercana")
        self.assertNotContains(response, ">✓<")
        self.assertNotContains(response, ">◉<")

    def test_home_keeps_its_query_budget(self):
        Product.objects.create(
            business=self.public_business,
            name="Chaquetas",
            slug="chaquetas",
            is_featured=True,
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

        with self.assertNumQueries(4):
            response = self.client.get(reverse("site:home"))

        self.assertEqual(response.status_code, 200)
