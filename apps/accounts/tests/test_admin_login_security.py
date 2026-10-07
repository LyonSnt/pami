from datetime import timedelta

from axes.models import AccessAttempt, AccessFailureLog
from django.contrib.auth import SESSION_KEY
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User


@override_settings(AXES_FAILURE_LIMIT=3)
class AdminLoginSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin-protegido", email="protected@example.com",
            password="Strong-local-test-password-71",
            is_staff=True,
        )
        self.url = reverse("admin:login")

    def post_login(self, password="wrong-password", client=None, username=None, **extra):
        return (client or self.client).post(
            self.url,
            {"username": username or self.user.username, "password": password},
            **extra,
        )

    def lock_user(self):
        for _ in range(3):
            response = self.post_login()
        return response

    def test_failed_logins_lock_even_correct_credentials_without_exposing_secrets(self):
        response = self.lock_user()
        self.assertEqual(response.status_code, 429)
        self.assertContains(response, "Acceso temporalmente bloqueado", status_code=429)
        self.assertEqual(response["Retry-After"], "900")
        self.assertIn("no-store", response["Cache-Control"])
        self.assertEqual(AccessFailureLog.objects.count(), 3)
        self.assertNotIn("wrong-password", str(list(AccessAttempt.objects.values())))
        self.assertNotContains(response, self.user.username, status_code=429)
        response = self.post_login(password="Strong-local-test-password-71")
        self.assertEqual(response.status_code, 429)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_changing_ip_cookie_or_user_agent_does_not_bypass_username_lockout(self):
        self.lock_user()
        response = self.post_login(
            client=Client(), password="Strong-local-test-password-71",
            REMOTE_ADDR="192.0.2.15", HTTP_USER_AGENT="another-browser",
            HTTP_X_FORWARDED_FOR="203.0.113.20",
        )
        self.assertEqual(response.status_code, 429)

    def test_attempts_during_lockout_do_not_extend_cooloff(self):
        self.lock_user()
        attempt = AccessAttempt.objects.get()
        blocked_at = attempt.attempt_time
        self.post_login()
        attempt.refresh_from_db()
        self.assertEqual(attempt.attempt_time, blocked_at)
        self.assertEqual(attempt.failures_since_start, 3)
        self.assertEqual(AccessFailureLog.objects.count(), 3)

    def test_cooloff_allows_login_again(self):
        self.lock_user()
        AccessAttempt.objects.update(attempt_time=timezone.now() - timedelta(minutes=16))
        response = self.post_login(password="Strong-local-test-password-71")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session[SESSION_KEY], str(self.user.pk))

    def test_success_before_limit_resets_failures(self):
        self.post_login()
        response = self.post_login(password="Strong-local-test-password-71")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(AccessAttempt.objects.filter(username=self.user.username).exists())

    def test_lockout_does_not_block_other_admin_or_public_pages(self):
        self.lock_user()
        other = User.objects.create_user(
            username="otro-admin", email="other@example.com", password="other-pass", is_staff=True,
        )
        response = self.post_login(username=other.username, password="other-pass", client=Client())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(reverse("site:home")).status_code, 200)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_recovery_command_unlocks_username(self):
        self.lock_user()
        call_command("axes_reset_username", self.user.username, verbosity=0)
        self.assertEqual(self.post_login(password="Strong-local-test-password-71").status_code, 302)

    def test_forwarded_headers_are_not_used_as_connection_ip(self):
        self.post_login(REMOTE_ADDR="192.0.2.10", HTTP_X_FORWARDED_FOR="203.0.113.20")
        self.assertEqual(AccessAttempt.objects.get().ip_address, "192.0.2.10")
