from django.test import TestCase
from django.urls import reverse

from apps.businesses.models import Business
from apps.portfolio.models import PortfolioProject


class PortfolioPublicViewTests(TestCase):
    def setUp(self):
        self.business = Business.objects.create(
            name="Negocio público",
            slug="negocio-publico",
            is_active=True,
            is_published=True,
        )

    def get_detail_url(self, project):
        return reverse(
            "portfolio:detail",
            kwargs={
                "business_slug": project.business.slug,
                "project_slug": project.slug,
            },
        )

    def test_detail_returns_404_for_unpublished_project(self):
        project = PortfolioProject.objects.create(
            business=self.business,
            title="Proyecto no publicado",
            slug="proyecto-no-publicado",
            is_active=True,
            is_published=False,
        )

        response = self.client.get(self.get_detail_url(project))

        self.assertEqual(response.status_code, 404)

    def test_detail_returns_404_when_business_is_inactive(self):
        project = PortfolioProject.objects.create(
            business=self.business,
            title="Proyecto público",
            slug="proyecto-publico",
            is_active=True,
            is_published=True,
        )
        self.business.is_active = False
        self.business.save(update_fields=["is_active", "updated_at"])

        response = self.client.get(self.get_detail_url(project))

        self.assertEqual(response.status_code, 404)
