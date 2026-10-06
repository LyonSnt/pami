from django.test import TestCase
from django.urls import reverse

from apps.businesses.models import Business


class BusinessPublicViewTests(TestCase):
    def create_public_business(self):
        return Business.objects.create(
            name="Creaciones",
            slug="creaciones",
            is_active=True,
            is_published=True,
        )

    def test_business_list_permanently_redirects_to_catalog(self):
        response = self.client.get(reverse("businesses:list"))

        self.assertRedirects(
            response,
            reverse("catalog:list"),
            status_code=301,
            fetch_redirect_response=False,
        )

    def test_business_detail_permanently_redirects_to_filtered_catalog(self):
        business = self.create_public_business()

        response = self.client.get(
            reverse("businesses:detail", kwargs={"slug": business.slug})
        )

        self.assertRedirects(
            response,
            reverse(
                "catalog:business_list",
                kwargs={"business_slug": business.slug},
            ),
            status_code=301,
            fetch_redirect_response=False,
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
