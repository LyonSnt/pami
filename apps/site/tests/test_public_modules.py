from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.portfolio.models import PortfolioProject
from apps.site.models import NavigationItem, SiteConfiguration


class PublicModuleVisibilityTests(TestCase):
    def setUp(self):
        self.configuration = SiteConfiguration.objects.create()
        self.business = Business.objects.create(
            name="Creaciones",
            slug="creaciones",
            is_active=True,
            is_published=True,
        )
        self.product = Product.objects.create(
            business=self.business,
            name="Chaquetas",
            slug="chaquetas",
            is_active=True,
            is_published=True,
        )
        self.project = PortfolioProject.objects.create(
            business=self.business,
            title="Colección de chaquetas",
            slug="coleccion-chaquetas",
            is_active=True,
            is_published=True,
        )
        self.post = BlogPost.objects.create(
            business=self.business,
            title="Cómo combinar chaquetas",
            slug="combinar-chaquetas",
            content="Contenido",
            published_at=timezone.now(),
            is_active=True,
            is_published=True,
        )

    def test_default_configuration_only_exposes_catalog(self):
        self.assertEqual(self.client.get(reverse("catalog:list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("portfolio:list")).status_code, 404)
        self.assertEqual(self.client.get(reverse("blog:list")).status_code, 404)
        self.assertEqual(self.client.get(reverse("contact:form")).status_code, 404)

    def test_disabled_module_uses_branded_404_even_with_debug_enabled(self):
        with self.settings(DEBUG=True):
            response = self.client.get(reverse("portfolio:list"))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "No encontramos esta página", status_code=404)
        self.assertNotContains(response, "Using the URLconf", status_code=404)

    def test_disabled_modules_are_removed_from_navigation_and_home(self):
        for order, (label, url) in enumerate(
            (
                ("Catálogo", "/catalogo/"),
                ("Portafolio", "/portafolio/"),
                ("Blog", "/blog/"),
                ("Contacto", "/contacto/"),
            ),
            start=1,
        ):
            NavigationItem.objects.create(label=label, url=url, order=order)

        response = self.client.get(reverse("site:home"))

        self.assertContains(response, "Catálogo")
        self.assertNotContains(response, "Portafolio")
        self.assertNotContains(response, ">Blog<", html=False)
        self.assertNotContains(response, "Contáctanos")
        self.assertNotContains(response, self.project.title)

    def test_footer_contact_details_remain_visible_when_form_is_disabled(self):
        self.configuration.email = "ventas@example.com"
        self.configuration.phone = "0991234567"
        self.configuration.whatsapp = "593991234567"
        self.configuration.address = "Ecuador"
        self.configuration.save(
            update_fields=("email", "phone", "whatsapp", "address", "updated_at")
        )

        response = self.client.get(reverse("site:home"))

        self.assertContains(response, 'href="mailto:ventas@example.com"')
        self.assertContains(response, 'href="tel:0991234567"')
        self.assertContains(response, 'href="https://wa.me/593991234567"')
        self.assertContains(response, "Ecuador")
        self.assertNotContains(response, reverse("contact:form"))

    def test_search_only_returns_content_from_enabled_modules(self):
        response = self.client.get(reverse("site:search"), {"q": "chaqueta"})

        self.assertContains(response, self.product.name)
        self.assertNotContains(response, self.project.title)
        self.assertNotContains(response, self.post.title)
        self.assertEqual(response.context["result_count"], 1)

    def test_sitemap_only_contains_enabled_modules(self):
        response = self.client.get(reverse("sitemap"))

        self.assertContains(response, reverse("catalog:list"))
        self.assertContains(
            response,
            reverse("catalog:business_list", args=[self.business.slug]),
        )
        self.assertNotContains(response, reverse("portfolio:list"))
        self.assertNotContains(response, reverse("blog:list"))
        self.assertNotContains(response, reverse("contact:form"))

    def test_modules_can_be_enabled_without_restoring_their_content(self):
        self.configuration.show_portfolio = True
        self.configuration.show_blog = True
        self.configuration.show_contact = True
        self.configuration.save(
            update_fields=(
                "show_portfolio",
                "show_blog",
                "show_contact",
                "updated_at",
            )
        )

        self.assertEqual(self.client.get(reverse("portfolio:list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("blog:list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("contact:form")).status_code, 200)

    def test_catalog_switch_disables_catalog_and_legacy_business_routes(self):
        self.configuration.show_catalog = False
        self.configuration.save(update_fields=("show_catalog", "updated_at"))

        self.assertEqual(self.client.get(reverse("catalog:list")).status_code, 404)
        self.assertEqual(self.client.get(reverse("businesses:list")).status_code, 404)
