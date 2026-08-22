from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

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

    def test_product_contact_action_includes_business_and_subject(self):
        product = Product.objects.create(
            business=self.business,
            name="Chaqueta urbana",
            slug="chaqueta-urbana",
            is_active=True,
            is_published=True,
        )

        response = self.client.get(self.get_detail_url(product))

        expected_url = (
            f"{reverse('contact:form')}?business={self.business.pk}"
            "&amp;subject=Consulta+sobre+Chaqueta+urbana"
        )
        self.assertContains(response, f'href="{expected_url}"')

    def test_product_generates_webp_card_variant_without_changing_original(self):
        source = BytesIO()
        Image.new("RGB", (800, 600), color="red").save(source, format="PNG")
        source.seek(0)

        with TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            product = Product.objects.create(
                business=self.business,
                name="Producto con imagen",
                slug="producto-con-imagen",
                image=SimpleUploadedFile(
                    "original.png",
                    source.read(),
                    content_type="image/png",
                ),
                is_active=True,
                is_published=True,
            )

            original_name = product.image.name
            product.image_card.generate()

            self.assertEqual(product.image.name, original_name)
            self.assertTrue(product.image_card.name.endswith(".webp"))
            self.assertEqual(product.image_card.width, 640)
            self.assertEqual(product.image_card.height, 480)
