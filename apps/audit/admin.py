from django.contrib import admin

from apps.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "user",
        "action",
        "app_label",
        "model_name",
        "object_repr",
        "ip_address",
    )
    list_filter = ("action", "app_label", "model_name", "created_at")
    search_fields = ("object_repr", "object_id", "user__username", "ip_address")
    readonly_fields = (
        "user",
        "action",
        "app_label",
        "model_name",
        "object_id",
        "object_repr",
        "ip_address",
        "user_agent",
        "metadata",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
