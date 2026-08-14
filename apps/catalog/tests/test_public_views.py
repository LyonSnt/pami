from django.test import TestCase
from django.urls import reverse

from apps.businesses.models import Business
from apps.catalog.models import Product


class ProductPublicViewTests(TestCase):
    def setUp(self):
        self.business = Business.objects.create(
            name="Negocio público",
            slug="negocio-publico",
            is_active=True,
            is_published=True,
        )

    def get_detail_url(self, product):
        return reverse(
            "catalog:detail",
            kwargs={
                "business_slug": product.business.slug,
                "product_slug": product.slug,
            },
        )

    def test_detail_returns_404_for_inactive_product(self):
        product = Product.objects.create(
            business=self.business,
            name="Producto inactivo",
            slug="producto-inactivo",
            is_active=False,
            is_published=True,
        )

        response = self.client.get(self.get_detail_url(product))

        self.assertEqual(response.status_code, 404)

    def test_detail_returns_404_when_business_is_unpublished(self):
        product = Product.objects.create(
            business=self.business,
            name="Producto público",
            slug="producto-publico",
            is_active=True,
            is_published=True,
        )
        self.business.is_published = False
        self.business.save(update_fields=["is_published", "updated_at"])

        response = self.client.get(self.get_detail_url(product))

        self.assertEqual(response.status_code, 404)

    def test_public_detail_marks_current_breadcrumb_item(self):
        product = Product.objects.create(
            business=self.business,
            name="Producto accesible",
            slug="producto-accesible",
            is_active=True,
            is_published=True,
        )

        response = self.client.get(self.get_detail_url(product))

        self.assertContains(response, 'aria-label="Migas de pan"')
        self.assertContains(response, 'aria-current="page"')
