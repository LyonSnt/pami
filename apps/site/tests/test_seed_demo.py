from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.site.models import NavigationItem, SiteConfiguration


class SeedDemoCommandTests(TestCase):
    def setUp(self):
        self.configuration = SiteConfiguration.objects.create(
            hero_title="Contenido anterior",
        )
        self.confections = Business.objects.create(
            name="Confecciones",
            slug="confecciones",
        )
        self.stationery = Business.objects.create(
            name="Papelería",
            slug="papeleria",
        )
        self.legacy_product = Product.objects.create(
            business=self.confections,
            name="Uniformes corporativos",
            slug="uniformes-corporativos",
        )
        self.legacy_navigation = NavigationItem.objects.create(
            label="Negocios",
            url="/negocios/",
        )

    def run_seed_demo(self):
        call_command("seed_demo", stdout=StringIO())

    def test_seed_updates_current_demo_without_duplicates(self):
        self.run_seed_demo()
        self.run_seed_demo()

        self.configuration.refresh_from_db()
        self.stationery.refresh_from_db()
        self.legacy_product.refresh_from_db()
        self.legacy_navigation.refresh_from_db()

        self.assertEqual(
            self.configuration.hero_title,
            "Chaquetas y buzos hechos para ti.",
        )
        self.assertEqual(
            self.configuration.slogan,
            "Donde encuentras todo para ti",
        )
        self.assertEqual(
            self.configuration.featured_business,
            self.confections,
        )
        self.assertFalse(self.stationery.is_published)
        self.assertFalse(self.legacy_product.is_published)
        self.assertFalse(self.legacy_navigation.is_active)

        products = Product.objects.filter(
            business=self.confections,
            slug__in=("chaquetas", "buzos"),
        )
        self.assertEqual(products.count(), 2)
        self.assertEqual(products.get(slug="chaquetas").order, 1)
        self.assertEqual(products.get(slug="buzos").order, 2)

        self.assertEqual(
            NavigationItem.objects.filter(label="Confecciones").count(),
            1,
        )
