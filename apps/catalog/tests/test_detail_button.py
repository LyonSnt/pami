from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.site.models import SiteConfiguration


class ProductDetailButtonTests(TestCase):
    def test_product_can_hide_and_restore_detail_button_in_home_and_catalog(self):
        business = Business.objects.create(name="Prendas", slug="prendas")
        SiteConfiguration.objects.create(featured_business=business)
        photo = BytesIO()
        Image.new("RGB", (200, 150), "blue").save(photo, format="PNG")
        with TemporaryDirectory() as directory, self.settings(MEDIA_ROOT=directory):
            product = Product.objects.create(
                business=business, name="Prenda de prueba", slug="prenda",
                is_featured=True,
                image=SimpleUploadedFile("detail-button-check.png", photo.getvalue(), content_type="image/png"),
            )
            detail_url = reverse("catalog:detail", args=[business.slug, product.slug])
            self.assertFalse(product.show_detail_button)
            for visible in (False, True, False):
                product.show_detail_button = visible
                product.save()
                for url in (reverse("site:home"), reverse("catalog:business_list", args=[business.slug])):
                    with self.subTest(visible=visible, url=url):
                        response = self.client.get(url)
                        self.assertContains(response, product.name)
                        self.assertContains(response, "Ver detalle", count=int(visible))
                        self.assertContains(response, f'href="{detail_url}"', count=int(visible))
                        self.assertContains(response, "data-image-zoom-trigger")
                self.assertContains(self.client.get(detail_url), product.name)
