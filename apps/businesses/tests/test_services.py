from django.test import TestCase

from apps.businesses.services.business import create_business


class BusinessServiceTests(TestCase):
    def test_model_generates_slug_when_service_creates_business(self):
        business = create_business(name="Negocio nuevo", slug="")

        self.assertEqual(business.slug, "negocio-nuevo")
