from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from apps.businesses.models import Business
from apps.catalog.models import Product, ProductFeature, ProductImage


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

    def test_detail_presents_only_active_generic_product_content(self):
        product = Product.objects.create(
            business=self.business,
            name="Sistema de gestión de agua",
            slug="sistema-gestion-agua",
            commercial_status=Product.CommercialStatus.QUOTE,
            target_audience="Juntas administradoras de agua.",
            additional_information="Incluye implementación y soporte.",
            demo_url="/contacto/",
            is_active=True,
            is_published=True,
        )
        active_feature = ProductFeature.objects.create(
            product=product,
            title="Gestión de lecturas",
            description="Registra consumos por medidor.",
            is_active=True,
        )
        ProductFeature.objects.create(
            product=product,
            title="Característica oculta",
            is_active=False,
        )

        response = self.client.get(self.get_detail_url(product))

        self.assertContains(response, "Bajo cotización")
        self.assertContains(response, "Juntas administradoras de agua")
        self.assertContains(response, "Incluye implementación y soporte")
        self.assertContains(response, "Ver demostración")
        self.assertContains(response, active_feature.title)
        self.assertNotContains(response, "Característica oculta")
        self.assertEqual(
            response.context["product"].public_features,
            [active_feature],
        )

    def test_detail_presents_only_active_gallery_images(self):
        product = Product.objects.create(
            business=self.business,
            name="Agenda",
            slug="agenda",
            is_active=True,
            is_published=True,
        )
        source = BytesIO()
        Image.new("RGB", (800, 600), color="blue").save(source, format="PNG")
        source.seek(0)

        with TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            active_image = ProductImage.objects.create(
                product=product,
                image=SimpleUploadedFile(
                    "agenda.png",
                    source.read(),
                    content_type="image/png",
                ),
                alt_text="Vista interior de la agenda",
                is_active=True,
            )
            ProductImage.objects.create(
                product=product,
                image=SimpleUploadedFile(
                    "oculta.png",
                    source.getvalue(),
                    content_type="image/png",
                ),
                alt_text="Imagen oculta",
                is_active=False,
            )

            response = self.client.get(self.get_detail_url(product))

        self.assertContains(response, "Galería")
        self.assertContains(response, active_image.alt_text)
        self.assertNotContains(response, "Imagen oculta")

    def test_general_catalog_presents_lines_without_mixing_products(self):
        digital_business = Business.objects.create(
            name="Soluciones digitales",
            slug="soluciones-digitales",
            is_active=True,
            is_published=True,
        )
        Product.objects.create(
            business=digital_business,
            name="Sistema de gestión de agua",
            slug="sistema-gestion-agua",
            is_active=True,
            is_published=True,
        )

        response = self.client.get(reverse("catalog:list"))

        self.assertContains(response, "Líneas de negocio")
        self.assertContains(response, self.business.name)
        self.assertContains(response, digital_business.name)
        self.assertNotContains(response, "Sistema de gestión de agua")
        self.assertContains(response, "Ver productos y servicios", count=2)
        self.assertContains(
            response,
            reverse(
                "catalog:business_list",
                kwargs={"business_slug": digital_business.slug},
            ),
        )

    def test_business_catalog_only_presents_products_from_selected_line(self):
        other_business = Business.objects.create(
            name="Papelería",
            slug="papeleria",
            is_active=True,
            is_published=True,
        )
        selected_product = Product.objects.create(
            business=self.business,
            name="Producto de la línea elegida",
            slug="producto-linea-elegida",
            is_active=True,
            is_published=True,
        )
        Product.objects.create(
            business=other_business,
            name="Producto de otra línea",
            slug="producto-otra-linea",
            is_active=True,
            is_published=True,
        )

        response = self.client.get(
            reverse(
                "catalog:business_list",
                kwargs={"business_slug": self.business.slug},
            )
        )

        self.assertContains(response, selected_product.name)
        self.assertNotContains(response, "Producto de otra línea")
