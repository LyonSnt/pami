from unittest.mock import Mock

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from apps.accounts.models import User
from apps.audit.admin import AuditLogAdmin
from apps.audit.models import AuditLog
from apps.businesses.admin import BusinessAdmin
from apps.businesses.models import Business


class AuditAdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="audit-admin",
            email="audit-admin@example.com",
            password="test-password",
        )
        self.request = RequestFactory().post("/admin/businesses/business/add/")
        self.request.user = self.user

    def test_model_admin_creation_is_audited(self):
        model_admin = BusinessAdmin(Business, AdminSite())
        business = Business(name="Negocio auditado", slug="negocio-auditado")
        form = Mock(changed_data=["name", "slug"])

        model_admin.save_model(self.request, business, form, change=False)

        audit_log = AuditLog.objects.get(
            action=AuditLog.Action.CREATE,
            object_id=str(business.pk),
        )
        self.assertEqual(audit_log.model_name, "business")
        self.assertEqual(audit_log.metadata["changed_fields"], ["name", "slug"])

    def test_audit_log_admin_is_immutable(self):
        model_admin = AuditLogAdmin(AuditLog, AdminSite())

        self.assertFalse(model_admin.has_add_permission(self.request))
        self.assertFalse(model_admin.has_change_permission(self.request))
        self.assertFalse(model_admin.has_delete_permission(self.request))
