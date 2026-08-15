from django.test import TestCase

from apps.accounts.models import User
from apps.audit.models import AuditLog


class AuthenticationAuditTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="editor-auditado",
            email="editor@example.com",
            password="test-password",
            is_staff=True,
        )

    def test_login_and_logout_are_audited(self):
        self.assertTrue(
            self.client.login(
                username=self.user.username,
                password="test-password",
            )
        )
        self.client.logout()

        actions = list(
            AuditLog.objects.filter(user=self.user)
            .order_by("created_at")
            .values_list("action", flat=True)
        )
        self.assertEqual(
            actions,
            [AuditLog.Action.LOGIN, AuditLog.Action.LOGOUT],
        )
