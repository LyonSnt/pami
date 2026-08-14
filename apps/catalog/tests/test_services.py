from django.test import TestCase

from apps.businesses.models import Business
from apps.catalog.services.product import create_product


class ProductServiceTests(TestCase):
    def test_model_generates_slug_when_service_creates_product(self):
        business = Business.objects.create(name="Negocio", slug="negocio")

        product = create_product(
            business=business,
            name="Producto nuevo",
            slug="",
        )

        self.assertEqual(product.slug, "producto-nuevo")
