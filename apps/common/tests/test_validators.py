from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.common.validators import (
    validate_file_size,
    validate_image_extension,
    validate_safe_link,
)
from apps.portfolio.models import PortfolioProject
from apps.site.models import SiteConfiguration


class FileValidatorTests(SimpleTestCase):
    def test_rejects_files_larger_than_five_megabytes(self):
        uploaded_file = Mock(size=(5 * 1024 * 1024) + 1)

        with self.assertRaisesMessage(ValidationError, "5 MB"):
            validate_file_size(uploaded_file)

    def test_rejects_unsupported_image_extensions(self):
        uploaded_file = Mock()
        uploaded_file.name = "imagen.gif"

        with self.assertRaisesMessage(ValidationError, "JPG, PNG o WEBP"):
            validate_image_extension(uploaded_file)

    def test_editorial_image_fields_use_both_upload_validators(self):
        image_fields = (
            (Business, "image"),
            (Product, "image"),
            (PortfolioProject, "image"),
            (BlogPost, "image"),
            (SiteConfiguration, "logo"),
            (SiteConfiguration, "favicon"),
            (SiteConfiguration, "hero_image"),
        )

        for model, field_name in image_fields:
            with self.subTest(model=model._meta.label, field=field_name):
                validators = model._meta.get_field(field_name).validators

                self.assertIn(validate_file_size, validators)
                self.assertIn(validate_image_extension, validators)


class SafeLinkValidatorTests(SimpleTestCase):
    def test_accepts_internal_paths_anchors_and_http_urls(self):
        valid_links = (
            "/catalogo/confecciones/",
            "#contenido",
            "https://example.com/confecciones",
            "http://example.com/contacto",
        )

        for link in valid_links:
            with self.subTest(link=link):
                validate_safe_link(link)

    def test_rejects_unsafe_or_ambiguous_links(self):
        invalid_links = (
            "javascript:alert(1)",
            "//example.com/ruta",
            "catalogo/confecciones/",
        )

        for link in invalid_links:
            with self.subTest(link=link):
                with self.assertRaises(ValidationError):
                    validate_safe_link(link)
