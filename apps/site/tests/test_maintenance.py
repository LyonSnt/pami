from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.site.models import SiteConfiguration


class MaintenanceModeTests(TestCase):
    def setUp(self):
        self.configuration = SiteConfiguration.objects.create(
            maintenance_mode=True,
        )

    def test_public_portal_returns_service_unavailable(self):
        response = self.client.get(reverse("site:home"))

        self.assertEqual(response.status_code, 503)
        self.assertContains(
            response,
            "Estamos realizando mejoras",
            status_code=503,
        )
        self.assertContains(
            response,
            'name="robots" content="noindex, nofollow"',
            status_code=503,
        )

    def test_admin_login_remains_available(self):
        response = self.client.get(reverse("admin:login"))

        self.assertEqual(response.status_code, 200)

    def test_static_and_media_paths_are_not_intercepted(self):
        static_response = self.client.get("/static/assets/branding/favicon.svg")
        media_response = self.client.get("/media/nonexistent-image.webp")

        self.assertNotEqual(static_response.status_code, 503)
        self.assertNotEqual(media_response.status_code, 503)

    def test_authenticated_staff_can_review_the_portal(self):
        staff_user = User.objects.create_user(
            username="staff-maintenance",
            email="staff-maintenance@example.com",
            password="test-password",
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.get(reverse("site:home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Estamos realizando mejoras")

    def test_portal_returns_normally_when_maintenance_is_disabled(self):
        self.configuration.maintenance_mode = False
        self.configuration.save(update_fields=("maintenance_mode", "updated_at"))

        response = self.client.get(reverse("site:home"))

        self.assertEqual(response.status_code, 200)
