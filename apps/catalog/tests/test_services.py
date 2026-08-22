from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.businesses.models import Business
from apps.catalog.models import Product, ProductFeature, ProductImage
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

    def test_product_supports_generic_commercial_information(self):
        business = Business.objects.create(
            name="Soluciones digitales",
            slug="soluciones-digitales",
        )
        product = Product(
            business=business,
            name="Sistema de gestión de agua",
            slug="sistema-gestion-agua",
            commercial_status=Product.CommercialStatus.QUOTE,
            target_audience="Juntas y empresas de agua.",
            additional_information="Aplicación web con implementación.",
            demo_url="/contacto/",
        )

        product.full_clean()

        self.assertEqual(product.get_commercial_status_display(), "Bajo cotización")

    def test_product_rejects_unsafe_demo_link(self):
        business = Business.objects.create(
            name="Sistemas",
            slug="sistemas-enlace",
        )
        product = Product(
            business=business,
            name="Sistema inseguro",
            slug="sistema-inseguro",
            demo_url="javascript:alert(1)",
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_relations_are_generic_and_use_accessible_fallback(self):
        business = Business.objects.create(name="Calzado", slug="calzado")
        product = Product.objects.create(
            business=business,
            name="Zapatos casuales",
            slug="zapatos-casuales",
        )
        feature = ProductFeature.objects.create(
            product=product,
            title="Material resistente",
        )
        gallery_image = ProductImage(
            product=product,
            image="catalog/products/gallery/zapatos.webp",
        )

        self.assertEqual(str(feature), "Zapatos casuales: Material resistente")
        self.assertEqual(gallery_image.accessible_alt, "Zapatos casuales")
