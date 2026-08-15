from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.businesses.models import Business
from apps.catalog.models import Product
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

    def test_visible_price_requires_a_value(self):
        business = Business.objects.create(name="Negocio", slug="negocio-precio")
        product = Product(
            business=business,
            name="Producto sin precio",
            slug="producto-sin-precio",
            show_price=True,
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Ingresa un precio para poder mostrarlo.",
        ):
            product.full_clean()

    def test_price_must_be_positive(self):
        business = Business.objects.create(name="Negocio", slug="negocio-positivo")
        product = Product(
            business=business,
            name="Producto negativo",
            slug="producto-negativo",
            price=Decimal("-1.00"),
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_database_rejects_visible_product_without_price(self):
        business = Business.objects.create(name="Negocio", slug="negocio-restriccion")

        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(
                business=business,
                name="Producto inválido",
                slug="producto-invalido",
                show_price=True,
            )
