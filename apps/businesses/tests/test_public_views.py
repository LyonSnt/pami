from django.test import TestCase
from django.urls import reverse

from apps.businesses.models import Business


class BusinessPublicViewTests(TestCase):
    def test_detail_links_to_business_catalog(self):
        business = Business.objects.create(
            name="Confecciones",
            slug="confecciones",
            is_active=True,
            is_published=True,
        )

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertContains(
            response,
            reverse(
                "catalog:business_list",
                kwargs={"business_slug": business.slug},
            ),
        )

    def test_detail_returns_404_for_inactive_business(self):
        business = Business.objects.create(
            name="Negocio inactivo",
            slug="negocio-inactivo",
            is_active=False,
            is_published=True,
        )

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertEqual(response.status_code, 404)

    def test_detail_returns_404_for_unpublished_business(self):
        business = Business.objects.create(
            name="Negocio no publicado",
            slug="negocio-no-publicado",
            is_active=True,
            is_published=False,
        )

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertEqual(response.status_code, 404)
