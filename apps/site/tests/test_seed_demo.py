from io import StringIO
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.portfolio.models import PortfolioProject
from apps.site.models import NavigationItem, SiteConfiguration


class SeedDemoCommandTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media_directory = TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.media_directory.name)
        cls.media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.media_override.disable()
        cls.media_directory.cleanup()

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
        self.assertTrue(products.get(slug="chaquetas").image)
        self.assertTrue(products.get(slug="buzos").image)
        self.assertTrue(self.configuration.hero_image)

        projects = PortfolioProject.objects.filter(
            business=self.confections,
            slug__in=("coleccion-inicial-chaquetas", "coleccion-inicial-buzos"),
        )
        self.assertEqual(projects.count(), 2)
        self.assertTrue(projects.get(slug="coleccion-inicial-chaquetas").image)
        self.assertTrue(projects.get(slug="coleccion-inicial-buzos").image)

        posts = BlogPost.objects.filter(
            business=self.confections,
            slug__in=("elegir-chaqueta-para-tu-estilo", "ideas-combinar-buzos"),
        )
        self.assertEqual(posts.count(), 2)
        self.assertTrue(posts.get(slug="elegir-chaqueta-para-tu-estilo").image)
        self.assertTrue(posts.get(slug="ideas-combinar-buzos").image)
        self.assertNotIn("Artículo demo", posts.get(slug="ideas-combinar-buzos").excerpt)

        self.assertEqual(
            NavigationItem.objects.filter(label="Confecciones").count(),
            1,
        )
