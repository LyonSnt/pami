from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log


@receiver(user_logged_in, dispatch_uid="audit_user_logged_in")
def audit_user_logged_in(sender, request, user, **kwargs):
    create_audit_log(
        request=request,
        user=user,
        action=AuditLog.Action.LOGIN,
        instance=user,
    )


@receiver(user_logged_out, dispatch_uid="audit_user_logged_out")
def audit_user_logged_out(sender, request, user, **kwargs):
    create_audit_log(
        request=request,
        user=user,
        action=AuditLog.Action.LOGOUT,
        instance=user,
    )
