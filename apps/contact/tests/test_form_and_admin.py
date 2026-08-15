from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.core import mail
from django.test import RequestFactory, TestCase, override_settings
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

    def test_form_includes_hidden_honeypot(self):
        response = self.client.get(reverse("contact:form"))

        self.assertContains(response, 'name="honeypot"')
        self.assertContains(response, 'type="hidden"')
        self.assertContains(response, 'aria-hidden="true"')

    def test_honeypot_submission_is_ignored_silently(self):
        response = self.client.post(
            reverse("contact:form"),
            {
                "name": "Robot",
                "email": "robot@example.com",
                "subject": "Publicidad",
                "message": "Contenido automatizado",
                "honeypot": "https://spam.example.com",
            },
        )

        self.assertRedirects(response, reverse("contact:success"))
        self.assertFalse(ContactMessage.objects.exists())
        self.assertFalse(AuditLog.objects.exists())

    def test_duplicate_submission_in_same_session_is_saved_once(self):
        submission = {
            "name": "Persona repetida",
            "email": "repetida@example.com",
            "subject": "Consulta repetida",
            "message": "El mismo mensaje.",
        }

        first_response = self.client.post(reverse("contact:form"), submission)
        second_response = self.client.post(reverse("contact:form"), submission)

        self.assertRedirects(first_response, reverse("contact:success"))
        self.assertRedirects(second_response, reverse("contact:success"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(
            AuditLog.objects.filter(action=AuditLog.Action.CREATE).count(),
            1,
        )

    def test_same_submission_is_allowed_after_duplicate_window(self):
        submission = {
            "name": "Persona recurrente",
            "email": "recurrente@example.com",
            "subject": "Consulta recurrente",
            "message": "El mismo contenido después de un tiempo.",
        }

        with patch(
            "apps.contact.services.submission.current_time",
            side_effect=(100, 100, 161, 161),
        ):
            self.client.post(reverse("contact:form"), submission)
            self.client.post(reverse("contact:form"), submission)

        self.assertEqual(ContactMessage.objects.count(), 2)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        CONTACT_NOTIFICATION_EMAIL="equipo@example.com",
    )
    def test_configured_recipient_receives_notification(self):
        response = self.client.post(
            reverse("contact:form"),
            {
                "name": "Persona notificada",
                "email": "persona@example.com",
                "subject": "Nueva consulta",
                "message": "Necesito información.",
            },
        )

        self.assertRedirects(response, reverse("contact:success"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["equipo@example.com"])
        self.assertIn("Nueva consulta", mail.outbox[0].subject)

    @override_settings(CONTACT_NOTIFICATION_EMAIL="equipo@example.com")
    def test_notification_failure_does_not_lose_message(self):
        with (
            patch(
                "apps.contact.services.notification.send_mail",
                side_effect=RuntimeError("SMTP no disponible"),
            ),
            self.assertLogs(
                "apps.contact.services.notification",
                level="ERROR",
            ),
        ):
            response = self.client.post(
                reverse("contact:form"),
                {
                    "name": "Persona conservada",
                    "email": "persona@example.com",
                    "subject": "Consulta conservada",
                    "message": "Este mensaje debe guardarse.",
                },
            )

        self.assertRedirects(response, reverse("contact:success"))
        self.assertEqual(ContactMessage.objects.count(), 1)


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

    def test_messages_cannot_be_created_deleted_or_reassigned_in_admin(self):
        user = User.objects.create_superuser(
            username="admin-contact-protection",
            email="admin-contact-protection@example.com",
            password="test-password",
        )
        request = RequestFactory().get("/admin/contact/contactmessage/")
        request.user = user
        model_admin = ContactMessageAdmin(ContactMessage, AdminSite())

        self.assertIn("business", model_admin.readonly_fields)
        self.assertFalse(model_admin.has_add_permission(request))
        self.assertFalse(model_admin.has_delete_permission(request))
