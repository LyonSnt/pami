import importlib

from django.core.exceptions import ImproperlyConfigured
from django.test import Client, SimpleTestCase, override_settings
from django.urls import clear_url_caches, reverse

from apps.accounts.tests import test_admin_login_security as login_tests
from apps.site.models import SiteConfiguration
from config.admin_path import normalize_admin_path


class AdminPathValidationTests(SimpleTestCase):
    def test_accepts_simple_path_with_optional_surrounding_slashes(self):
        for value in ("panel-pami", "panel-pami/", "/panel-pami/", " panel-pami "):
            self.assertEqual(normalize_admin_path(value), "panel-pami/")

    def test_rejects_empty_nested_unsafe_or_conflicting_paths(self):
        for value in ("", "/", "a/b", "../panel", "panel?x=1", "https://panel", "panel name", "catalogo", "STATIC"):
            with self.subTest(value=value), self.assertRaises(ImproperlyConfigured):
                normalize_admin_path(value)


class CustomAdminPathTests(login_tests.AdminLoginSecurityTests):
    """Exercise the same login protections against the real URLconf at a new path."""

    def setUp(self):
        import config.urls.public as public_urls

        configuration = override_settings(ADMIN_URL_PATH="panel-prueba/")
        configuration.enable()

        def restore_urls():
            configuration.disable()
            importlib.reload(public_urls)
            clear_url_caches()

        self.addCleanup(restore_urls)
        importlib.reload(public_urls)
        clear_url_caches()
        super().setUp()

    def test_admin_links_and_login_use_custom_path(self):
        self.assertEqual(reverse("admin:index"), "/panel-prueba/")
        self.assertEqual(self.url, "/panel-prueba/login/")
        response = self.client.get(reverse("admin:index"))
        self.assertRedirects(response, "/panel-prueba/login/?next=/panel-prueba/")
        self.assertEqual(self.post_login(password="Strong-local-test-password-71").status_code, 302)
        self.assertContains(self.client.get(reverse("admin:index")), "/panel-prueba/logout/")

    def test_old_admin_urls_return_404_without_redirect(self):
        for debug in (True, False):
            with override_settings(DEBUG=debug):
                for url in ("/admin", "/admin/", "/admin/login/", "/admin/accounts/user/"):
                    for method in ("get", "post"):
                        with self.subTest(debug=debug, url=url, method=method):
                            response = getattr(Client(enforce_csrf_checks=True), method)(url)
                            self.assertContains(response, "Página no disponible", status_code=404)
                            self.assertContains(response, "Esta dirección no está disponible. Puedes volver al inicio para continuar.", status_code=404)
                            self.assertContains(response, "Volver al inicio", status_code=404)
                            self.assertNotContains(response, "Buscar en Pámi", status_code=404)
                            self.assertNotContains(response, 'href="/buscar/"', status_code=404)
                            self.assertNotIn("Location", response)
                            self.assertNotContains(response, "Using the URLconf", status_code=404)
                            self.assertNotContains(response, "panel-prueba", status_code=404)

    def test_custom_login_remains_available_during_maintenance(self):
        SiteConfiguration.objects.create(maintenance_mode=True)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.assertEqual(self.client.get(reverse("site:home")).status_code, 503)
        self.assertContains(self.client.get("/admin/login/"), "Página no disponible", status_code=404)
        self.assertEqual(self.lock_user().status_code, 429)

    def test_robots_does_not_publish_custom_admin_path(self):
        response = self.client.get(reverse("robots"))
        self.assertNotContains(response, "panel-prueba")
        self.assertNotContains(response, "/admin/")
        self.assertContains(self.client.get(self.url), 'name="robots"')
