from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from apps.accounts.models import User
from apps.site.admin import SiteConfigurationAdmin
from apps.site.models import SiteConfiguration


class SiteConfigurationAdminTests(TestCase):
    def test_add_is_disabled_when_configuration_exists(self):
        SiteConfiguration.objects.create()
        request = RequestFactory().get("/admin/site/siteconfiguration/add/")
        request.user = User(is_staff=True, is_superuser=True)
        model_admin = SiteConfigurationAdmin(SiteConfiguration, AdminSite())

        self.assertFalse(model_admin.has_add_permission(request))
