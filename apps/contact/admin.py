from django.contrib import admin

from apps.audit.admin_mixins import AuditModelAdminMixin
from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log
from apps.contact.models import ContactMessage
from apps.contact.services.message import (
    close_contact_message,
    mark_contact_message_in_review,
    mark_contact_message_responded,
)


@admin.register(ContactMessage)
class ContactMessageAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("name", "email", "business", "subject", "status", "created_at")
    list_filter = ("business", "status", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    autocomplete_fields = ("business",)
    readonly_fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "status",
        "responded_at",
        "created_at",
    )
    actions = (
        "mark_in_review",
        "mark_responded",
        "mark_closed",
    )

    fieldsets = (
        ("Datos del mensaje", {
            "fields": ("business", "name", "email", "phone", "subject", "message")
        }),
        ("Gestión", {
            "fields": ("status", "responded_at")
        }),
        ("Auditoría", {
            "fields": ("created_at",)
        }),
    )

    def _apply_transition(self, request, queryset, transition, transition_name):
        updated = 0
        for message in queryset.iterator():
            transition(message)
            create_audit_log(
                request=request,
                action=AuditLog.Action.UPDATE,
                instance=message,
                metadata={"transition": transition_name},
            )
            updated += 1

        self.message_user(request, f"Mensajes actualizados: {updated}.")

    @admin.action(description="Marcar como en revisión")
    def mark_in_review(self, request, queryset):
        self._apply_transition(
            request,
            queryset,
            mark_contact_message_in_review,
            ContactMessage.Status.IN_REVIEW,
        )

    @admin.action(description="Marcar como respondido")
    def mark_responded(self, request, queryset):
        self._apply_transition(
            request,
            queryset,
            mark_contact_message_responded,
            ContactMessage.Status.RESPONDED,
        )

    @admin.action(description="Marcar como cerrado")
    def mark_closed(self, request, queryset):
        self._apply_transition(
            request,
            queryset,
            close_contact_message,
            ContactMessage.Status.CLOSED,
        )
