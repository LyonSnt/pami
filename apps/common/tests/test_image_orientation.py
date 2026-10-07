from io import BytesIO
from tempfile import TemporaryDirectory
from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from imagekit.processors import ResizeToFill
from imagekit.specs import ImageSpec
from PIL import Image

from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.common.images import WEBP_OPTIONS


class ResponsiveImageOrientationTests(TestCase):
    colors = ((240, 20, 20), (20, 220, 20), (20, 20, 240), (240, 220, 20))

    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.media_override = self.settings(MEDIA_ROOT=directory.name)
        self.media_override.enable()
        self.addCleanup(self.media_override.disable)
        self.business = Business.objects.create(name="Prendas", slug="prendas")

    def create_photo(self, orientation=None, format="JPEG", size=(400, 300)):
        image = Image.new("RGB", size)
        width, height = size
        boxes = (
            (0, 0, width // 2, height // 2), (width // 2, 0, width, height // 2),
            (0, height // 2, width // 2, height), (width // 2, height // 2, width, height),
        )
        for color, box in zip(self.colors, boxes):
            image.paste(color, box)
        options = {}
        if orientation is not None:
            exif = Image.Exif()
            exif[274] = orientation
            options["exif"] = exif
        output = BytesIO()
        image.save(output, format=format, **options)
        raw = output.getvalue()
        extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[format]
        product = Product.objects.create(
            business=self.business, name="Foto", slug=f"foto-{Product.objects.count()}",
            image=SimpleUploadedFile(f"photo-{uuid4().hex[:16]}.{extension}", raw, content_type=f"image/{extension}"),
        )
        return product, raw

    def assert_corners(self, variant, expected):
        variant.generate()
        with variant.storage.open(variant.name, "rb") as file, Image.open(file) as image:
            self.assertEqual(image.format, "WEBP")
            width, height = image.size
            for point, label in zip(
                ((width // 8, height // 8), (7 * width // 8, height // 8),
                 (width // 8, 7 * height // 8), (7 * width // 8, 7 * height // 8)),
                expected,
            ):
                pixel = image.convert("RGB").getpixel(point)
                closest = min(range(4), key=lambda index: sum((a - b) ** 2 for a, b in zip(pixel, self.colors[index])))
                self.assertEqual(closest, label)
            self.assertNotIn(image.getexif().get(274), (2, 3, 4, 5, 6, 7, 8))

    def test_all_exif_orientations_are_applied_before_card_and_detail_crop(self):
        expected = {
            1: (0, 1, 2, 3), 2: (1, 0, 3, 2), 3: (3, 2, 1, 0),
            4: (2, 3, 0, 1), 5: (0, 2, 1, 3), 6: (2, 0, 3, 1),
            7: (3, 1, 2, 0), 8: (1, 3, 0, 2),
        }
        for orientation, corners in expected.items():
            with self.subTest(orientation=orientation):
                product, raw = self.create_photo(orientation)
                for variant in (product.image_card_small, product.image_card, product.image_detail):
                    self.assert_corners(variant, corners)
                with product.image.storage.open(product.image.name, "rb") as original:
                    self.assertEqual(original.read(), raw)

    def test_png_and_webp_orientation_is_also_applied(self):
        for format in ("PNG", "WEBP"):
            with self.subTest(format=format):
                product, _ = self.create_photo(6, format=format)
                self.assert_corners(product.image_card, (2, 0, 3, 1))

    def test_photos_without_exif_keep_their_orientation(self):
        for size in ((400, 300), (300, 400)):
            with self.subTest(size=size):
                product, _ = self.create_photo(size=size)
                self.assert_corners(product.image_card, (0, 1, 2, 3))

    def test_existing_images_use_a_new_cache_path_without_changing_original(self):
        product, raw = self.create_photo(6)
        old_spec = ImageSpec(source=product.image)
        old_spec.processors = [ResizeToFill(640, 480)]
        old_spec.format = "WEBP"
        old_spec.options = WEBP_OPTIONS
        previous_name = old_spec.cachefile_name
        product.image.storage.save(previous_name, ContentFile(old_spec.generate().read()))
        self.assertNotEqual(product.image_card.name, previous_name)
        self.assert_corners(product.image_card, (2, 0, 3, 1))
        self.assertTrue(product.image.storage.exists(previous_name))
        with product.image.storage.open(product.image.name, "rb") as original:
            self.assertEqual(original.read(), raw)
