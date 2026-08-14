from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.audit.models import AuditLog
from apps.businesses.models import Business
from apps.contact.admin import ContactMessageAdmin
from apps.contact.forms import ContactMessageForm
from apps.contact.models import ContactMessage


class ContactMessageFormTests(TestCase):
    def test_form_renders_explicit_accessible_controls_and_submit_button(self):
        response = self.client.get(reverse("contact:form"))

        self.assertContains(response, 'for="id_name"')
        self.assertContains(response, 'class="w-full rounded-lg border border-slate-300')
        self.assertContains(response, '<button\n    type="submit"', html=False)
        self.assertNotContains(response, "form.as_p")

    def test_business_field_only_contains_public_businesses(self):
        public_business = Business.objects.create(
            name="Negocio público",
            slug="negocio-publico",
            is_active=True,
            is_published=True,
        )
        Business.objects.create(
            name="Negocio oculto",
            slug="negocio-oculto",
            is_active=False,
            is_published=True,
        )

        form = ContactMessageForm()

        self.assertQuerySetEqual(
            form.fields["business"].queryset,
            [public_business],
        )

    def test_valid_submission_creates_message_and_audit_log(self):
        response = self.client.post(
            reverse("contact:form"),
            {
                "name": "Persona de prueba",
                "email": "persona@example.com",
                "phone": "0999999999",
                "subject": "Consulta",
                "message": "Necesito más información.",
            },
        )

        message = ContactMessage.objects.get()
        audit_log = AuditLog.objects.get(
            action=AuditLog.Action.CREATE,
            object_id=str(message.pk),
        )
        self.assertRedirects(response, reverse("contact:success"))
        self.assertEqual(audit_log.model_name, "contactmessage")

    def test_success_message_is_announced(self):
        response = self.client.post(
            reverse("contact:form"),
            {
                "name": "Persona de prueba",
                "email": "persona@example.com",
                "subject": "Consulta accesible",
                "message": "Necesito más información.",
            },
            follow=True,
        )

        self.assertContains(response, 'aria-live="polite"')
        self.assertContains(response, 'role="status"')

    def test_invalid_field_is_connected_to_its_error(self):
        response = self.client.post(
            reverse("contact:form"),
            {
                "name": "",
                "email": "correo-invalido",
                "subject": "",
                "message": "",
            },
        )

        self.assertContains(response, 'aria-invalid="true"')
        self.assertContains(response, 'aria-describedby="id_name_errors"')
        self.assertContains(response, 'id="id_name_errors"')


class ContactMessageAdminTests(TestCase):
    def test_mark_responded_uses_transition_and_creates_audit_log(self):
        message = ContactMessage.objects.create(
            name="Persona de prueba",
            email="persona@example.com",
            subject="Consulta",
            message="Mensaje",
        )
        user = User.objects.create_superuser(
            username="admin-contact",
            email="admin-contact@example.com",
            password="test-password",
        )
        request = RequestFactory().post("/admin/contact/contactmessage/")
        request.user = user
        model_admin = ContactMessageAdmin(ContactMessage, AdminSite())

        with patch.object(model_admin, "message_user"):
            model_admin.mark_responded(
                request,
                ContactMessage.objects.filter(pk=message.pk),
            )

        message.refresh_from_db()
        self.assertEqual(message.status, ContactMessage.Status.RESPONDED)
        self.assertIsNotNone(message.responded_at)
        self.assertTrue(
            AuditLog.objects.filter(
                action=AuditLog.Action.UPDATE,
                object_id=str(message.pk),
                metadata={"transition": ContactMessage.Status.RESPONDED},
            ).exists()
        )
