from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log


class AuditModelAdminMixin:
    @staticmethod
    def _get_instance_data(obj):
        return {
            "app_label": obj._meta.app_label,
            "model_name": obj._meta.model_name,
            "object_id": str(obj.pk or ""),
            "object_repr": str(obj),
        }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        metadata = {}
        if form is not None and form.changed_data:
            metadata["changed_fields"] = list(form.changed_data)

        create_audit_log(
            request=request,
            action=AuditLog.Action.UPDATE if change else AuditLog.Action.CREATE,
            instance=obj,
            metadata=metadata,
        )

    def delete_model(self, request, obj):
        instance_data = self._get_instance_data(obj)
        super().delete_model(request, obj)
        create_audit_log(
            request=request,
            action=AuditLog.Action.DELETE,
            **instance_data,
        )

    def delete_queryset(self, request, queryset):
        instances_data = [
            self._get_instance_data(obj)
            for obj in queryset.iterator()
        ]
        super().delete_queryset(request, queryset)

        for instance_data in instances_data:
            create_audit_log(
                request=request,
                action=AuditLog.Action.DELETE,
                **instance_data,
            )
