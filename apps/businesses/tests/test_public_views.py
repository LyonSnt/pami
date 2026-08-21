from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.portfolio.models import PortfolioProject


class BusinessPublicViewTests(TestCase):
    def create_public_business(self):
        return Business.objects.create(
            name="Confecciones",
            slug="confecciones",
            is_active=True,
            is_published=True,
        )

    def test_detail_links_to_business_catalog(self):
        business = self.create_public_business()

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertContains(
            response,
            reverse(
                "catalog:business_list",
                kwargs={"business_slug": business.slug},
            ),
        )

    def test_detail_presents_published_related_content(self):
        business = self.create_public_business()
        product = Product.objects.create(
            business=business,
            name="Chaquetas",
            slug="chaquetas",
            is_active=True,
            is_published=True,
        )
        project = PortfolioProject.objects.create(
            business=business,
            title="Colección de chaquetas",
            slug="coleccion-chaquetas",
            is_active=True,
            is_published=True,
        )
        post = BlogPost.objects.create(
            business=business,
            title="Cómo elegir una chaqueta",
            slug="elegir-chaqueta",
            content="Contenido publicado.",
            published_at=timezone.now(),
            is_active=True,
            is_published=True,
        )

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertContains(response, "Productos de Confecciones")
        self.assertContains(response, product.name)
        self.assertContains(response, "Trabajos realizados")
        self.assertContains(response, project.title)
        self.assertContains(response, "Ideas y novedades")
        self.assertContains(response, post.title)
        self.assertContains(response, 'aria-label="Migas de pan"')

    def test_detail_excludes_unpublished_related_content(self):
        business = self.create_public_business()
        Product.objects.create(
            business=business,
            name="Producto oculto",
            slug="producto-oculto",
            is_active=True,
            is_published=False,
        )
        PortfolioProject.objects.create(
            business=business,
            title="Proyecto oculto",
            slug="proyecto-oculto",
            is_active=False,
            is_published=True,
        )
        BlogPost.objects.create(
            business=business,
            title="Artículo futuro",
            slug="articulo-futuro-linea",
            content="Contenido futuro.",
            published_at=timezone.now() + timedelta(days=1),
            is_active=True,
            is_published=True,
        )

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertNotContains(response, "Producto oculto")
        self.assertNotContains(response, "Proyecto oculto")
        self.assertNotContains(response, "Artículo futuro")
        self.assertContains(response, "Contenido en preparación")

    def test_detail_keeps_its_query_budget(self):
        business = self.create_public_business()
        Product.objects.create(
            business=business,
            name="Chaquetas",
            slug="chaquetas",
            is_active=True,
            is_published=True,
        )
        PortfolioProject.objects.create(
            business=business,
            title="Colección inicial",
            slug="coleccion-inicial",
            is_active=True,
            is_published=True,
        )
        BlogPost.objects.create(
            business=business,
            title="Artículo relacionado",
            slug="articulo-relacionado",
            content="Contenido.",
            published_at=timezone.now(),
            is_active=True,
            is_published=True,
        )

        with self.assertNumQueries(6):
            response = self.client.get(
                reverse("businesses:detail", kwargs={"slug": business.slug})
            )

        self.assertEqual(response.status_code, 200)

    def test_detail_returns_404_for_inactive_business(self):
        business = Business.objects.create(
            name="Negocio inactivo",
            slug="negocio-inactivo",
            is_active=False,
            is_published=True,
        )

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertEqual(response.status_code, 404)

    def test_detail_returns_404_for_unpublished_business(self):
        business = Business.objects.create(
            name="Negocio no publicado",
            slug="negocio-no-publicado",
            is_active=True,
            is_published=False,
        )

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertEqual(response.status_code, 404)
