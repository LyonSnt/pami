from django.test import TestCase

from apps.businesses.models import Business
from apps.portfolio.services.project import create_portfolio_project


class PortfolioServiceTests(TestCase):
    def test_model_generates_slug_when_service_creates_project(self):
        business = Business.objects.create(name="Negocio", slug="negocio")

        project = create_portfolio_project(
            business=business,
            title="Proyecto nuevo",
            slug="",
        )

        self.assertEqual(project.slug, "proyecto-nuevo")
