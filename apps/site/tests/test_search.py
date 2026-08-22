from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product, ProductFeature
from apps.portfolio.models import PortfolioProject


class SearchViewTests(TestCase):
    def setUp(self):
        self.business = Business.objects.create(
            name="Confecciones",
            slug="confecciones",
            short_description="Prendas para todos los días",
            is_active=True,
            is_published=True,
        )

    def test_search_groups_matching_public_content(self):
        product = Product.objects.create(
            business=self.business,
            name="Chaqueta urbana",
            slug="chaqueta-urbana",
            is_active=True,
            is_published=True,
        )
        project = PortfolioProject.objects.create(
            business=self.business,
            title="Colección de chaquetas",
            slug="coleccion-chaquetas",
            is_active=True,
            is_published=True,
        )
        post = BlogPost.objects.create(
            business=self.business,
            title="Cómo combinar una chaqueta",
            slug="combinar-chaqueta",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now(),
        )

        response = self.client.get(reverse("site:search"), {"q": "chaqueta"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)
        self.assertContains(response, project.title)
        self.assertContains(response, post.title)
        self.assertContains(response, "Productos")
        self.assertContains(response, "Proyectos")
        self.assertContains(response, "Artículos")
        self.assertEqual(response.context["result_count"], 3)

    def test_search_excludes_hidden_and_future_content(self):
        Product.objects.create(
            business=self.business,
            name="Chaqueta oculta",
            slug="chaqueta-oculta",
            is_active=True,
            is_published=False,
        )
        BlogPost.objects.create(
            title="Chaqueta futura",
            slug="chaqueta-futura",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now() + timedelta(days=1),
        )

        response = self.client.get(reverse("site:search"), {"q": "chaqueta"})

        self.assertNotContains(response, "Chaqueta oculta")
        self.assertNotContains(response, "Chaqueta futura")
        self.assertEqual(response.context["result_count"], 0)

    def test_empty_query_shows_initial_guidance(self):
        response = self.client.get(reverse("site:search"))

        self.assertContains(response, "Escribe lo que deseas encontrar")
        self.assertEqual(response.context["result_count"], 0)

    def test_no_results_shows_empty_state(self):
        response = self.client.get(reverse("site:search"), {"q": "inexistente"})

        self.assertContains(response, "No encontramos resultados")
        self.assertContains(response, "0 resultados")

    def test_search_is_accessible_and_not_indexed(self):
        response = self.client.get(reverse("site:search"), {"q": "buzos"})

        self.assertContains(response, 'role="search"')
        self.assertContains(response, 'aria-live="polite"')
        self.assertContains(response, 'name="robots" content="noindex, follow"')
        self.assertContains(
            response,
            'rel="canonical" href="http://testserver/buscar/"',
        )

    def test_header_links_to_search_in_desktop_and_mobile(self):
        response = self.client.get(reverse("site:home"))

        self.assertContains(response, reverse("site:search"), count=2)
        self.assertContains(response, 'aria-label="Buscar en Pámi"')

    def test_search_keeps_its_query_budget(self):
        with self.assertNumQueries(6):
            response = self.client.get(
                reverse("site:search"),
                {"q": "confecciones"},
            )

        self.assertEqual(response.status_code, 200)

    def test_search_finds_product_by_active_feature(self):
        product = Product.objects.create(
            business=self.business,
            name="Sistema de gestión de agua",
            slug="sistema-gestion-agua",
            is_active=True,
            is_published=True,
        )
        ProductFeature.objects.create(
            product=product,
            title="Facturación de consumos",
            is_active=True,
        )

        response = self.client.get(reverse("site:search"), {"q": "facturación"})

        self.assertContains(response, product.name)
        self.assertEqual(response.context["result_count"], 1)
