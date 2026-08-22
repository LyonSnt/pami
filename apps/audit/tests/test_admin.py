from io import BytesIO
from unittest.mock import Mock, patch

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.audit.admin import AuditLogAdmin
from apps.audit.models import AuditLog
from apps.audit.services.backup import (
    DatabaseBackupError,
    DatabaseBackupResult,
)
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

    def test_audit_log_is_visible_only_to_superusers(self):
        model_admin = AuditLogAdmin(AuditLog, AdminSite())
        staff_user = User.objects.create_user(
            username="staff-sin-auditoria",
            email="staff@example.com",
            password="test-password",
            is_staff=True,
        )
        staff_request = RequestFactory().get("/admin/audit/auditlog/")
        staff_request.user = staff_user

        self.assertTrue(model_admin.has_view_permission(self.request))
        self.assertFalse(model_admin.has_view_permission(staff_request))


class DatabaseBackupAdminTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="backup-admin",
            email="backup-admin@example.com",
            password="test-password",
        )
        self.staff_user = User.objects.create_user(
            username="backup-staff",
            email="backup-staff@example.com",
            password="test-password",
            is_staff=True,
        )
        self.url = reverse("admin:audit_databasebackup_changelist")

    def test_backup_page_is_visible_to_superuser(self):
        self.client.force_login(self.superuser)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crear y descargar respaldo")
        self.assertContains(response, "no incluye las imágenes")

    def test_backup_page_rejects_regular_staff_user(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    @patch("apps.audit.admin.create_database_backup")
    def test_superuser_downloads_uncached_backup_and_operation_is_audited(
        self,
        create_backup,
    ):
        create_backup.return_value = DatabaseBackupResult(
            file=BytesIO(b"PGDMP-test-backup"),
            filename="pami_db_2026-08-21_120000.dump",
            size=17,
        )
        self.client.force_login(self.superuser)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("no-store", response["Cache-Control"])
        self.assertIn("private", response["Cache-Control"])
        self.assertIn(
            'attachment; filename="pami_db_2026-08-21_120000.dump"',
            response["Content-Disposition"],
        )
        self.assertEqual(b"".join(response.streaming_content), b"PGDMP-test-backup")
        audit_log = AuditLog.objects.get(model_name="database_backup")
        self.assertEqual(audit_log.user, self.superuser)
        self.assertEqual(audit_log.metadata["status"], "completed")
        self.assertEqual(audit_log.metadata["size"], 17)

    @patch("apps.audit.admin.create_database_backup")
    def test_backup_failure_is_reported_and_audited(self, create_backup):
        create_backup.side_effect = DatabaseBackupError(
            "No se pudo generar el respaldo."
        )
        self.client.force_login(self.superuser)

        response = self.client.post(self.url)

        self.assertRedirects(response, self.url)
        audit_log = AuditLog.objects.get(model_name="database_backup")
        self.assertEqual(audit_log.metadata["status"], "failed")
