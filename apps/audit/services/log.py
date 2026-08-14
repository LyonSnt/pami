from apps.audit.models import AuditLog
from apps.audit.utils import get_client_ip, get_user_agent


def create_audit_log(
    *,
    request=None,
    user=None,
    action,
    instance=None,
    app_label="",
    model_name="",
    object_id="",
    object_repr="",
    ip_address=None,
    user_agent="",
    metadata=None,
):
    if request is not None:
        user = getattr(request, "user", None)
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)

    if instance is not None:
        app_label = instance._meta.app_label
        model_name = instance._meta.model_name
        object_id = str(instance.pk or "")
        object_repr = str(instance)

    return AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        app_label=app_label,
        model_name=model_name,
        object_id=object_id,
        object_repr=object_repr,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata or {},
    )