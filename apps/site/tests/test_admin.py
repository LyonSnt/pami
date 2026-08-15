from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase

from apps.accounts.models import User
from apps.blog.admin import BlogPostAdmin
from apps.blog.models import BlogPost
from apps.businesses.admin import BusinessAdmin
from apps.businesses.models import Business
from apps.catalog.admin import ProductAdmin
from apps.catalog.models import Product
from apps.portfolio.admin import PortfolioProjectAdmin
from apps.portfolio.models import PortfolioProject
from apps.site.admin import SiteConfigurationAdmin
from apps.site.models import NavigationItem, SiteConfiguration


class SiteConfigurationAdminTests(TestCase):
    def test_add_is_disabled_when_configuration_exists(self):
        SiteConfiguration.objects.create()
        request = RequestFactory().get("/admin/site/siteconfiguration/add/")
        request.user = User(is_staff=True, is_superuser=True)
        model_admin = SiteConfigurationAdmin(SiteConfiguration, AdminSite())

        self.assertFalse(model_admin.has_add_permission(request))

    def test_delete_is_always_disabled(self):
        configuration = SiteConfiguration.objects.create()
        request = RequestFactory().get("/admin/site/siteconfiguration/")
        request.user = User(is_staff=True, is_superuser=True)
        model_admin = SiteConfigurationAdmin(SiteConfiguration, AdminSite())

        self.assertFalse(model_admin.has_delete_permission(request))
        self.assertFalse(
            model_admin.has_delete_permission(request, configuration)
        )


class EditorialAdminTests(TestCase):
    def test_active_status_is_available_in_editorial_admins(self):
        admin_site = AdminSite()
        model_admin_pairs = (
            (BusinessAdmin, Business),
            (ProductAdmin, Product),
            (PortfolioProjectAdmin, PortfolioProject),
            (BlogPostAdmin, BlogPost),
        )

        for admin_class, model in model_admin_pairs:
            with self.subTest(model=model._meta.label):
                model_admin = admin_class(model, admin_site)
                fieldset_fields = {
                    field
                    for _, options in model_admin.fieldsets
                    for field in options["fields"]
                }

                self.assertIn("is_active", model_admin.list_display)
                self.assertIn("is_active", model_admin.list_filter)
                self.assertIn("is_active", fieldset_fields)


class EditorialLinkValidationTests(TestCase):
    def test_navigation_rejects_unsafe_protocol(self):
        item = NavigationItem(label="Enlace", url="javascript:alert(1)")

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_site_configuration_rejects_unsafe_hero_link(self):
        configuration = SiteConfiguration(
            hero_primary_button_url="javascript:alert(1)",
        )

        with self.assertRaises(ValidationError):
            configuration.full_clean()
