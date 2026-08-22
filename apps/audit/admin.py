from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from apps.audit.models import AuditLog, DatabaseBackup
from apps.audit.services.backup import DatabaseBackupError, create_database_backup
from apps.audit.services.log import create_audit_log


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

    def has_view_permission(self, request, obj=None):
        return bool(request.user.is_active and request.user.is_superuser)


@admin.register(DatabaseBackup)
class DatabaseBackupAdmin(admin.ModelAdmin):
    change_list_template = "admin/audit/database_backup.html"

    def has_module_permission(self, request):
        return bool(request.user.is_active and request.user.is_superuser)

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if not self.has_view_permission(request):
            raise PermissionDenied

        if request.method == "POST":
            return self._download_backup(request)

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "Respaldo de base de datos",
            "has_view_permission": True,
        }
        if extra_context:
            context.update(extra_context)
        return TemplateResponse(request, self.change_list_template, context)

    def _download_backup(self, request):
        try:
            backup = create_database_backup()
        except DatabaseBackupError as error:
            create_audit_log(
                request=request,
                action=AuditLog.Action.OTHER,
                app_label="audit",
                model_name="database_backup",
                object_repr="Respaldo de base de datos fallido",
                metadata={"status": "failed"},
            )
            self.message_user(request, str(error), level=messages.ERROR)
            return HttpResponseRedirect(request.path)

        create_audit_log(
            request=request,
            action=AuditLog.Action.OTHER,
            app_label="audit",
            model_name="database_backup",
            object_repr="Respaldo de base de datos descargado",
            metadata={
                "status": "completed",
                "filename": backup.filename,
                "size": backup.size,
            },
        )
        response = FileResponse(
            backup.file,
            as_attachment=True,
            filename=backup.filename,
            content_type="application/octet-stream",
        )
        response["Cache-Control"] = "no-store, private"
        response["Pragma"] = "no-cache"
        return response
