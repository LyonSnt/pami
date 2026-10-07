from ipaddress import ip_address

from django.conf import settings
from django.contrib import admin
from django.shortcuts import render


def get_connection_ip(request):
    """Do not trust forwarded headers supplied by clients or unknown proxies."""
    value = request.META.get("REMOTE_ADDR")
    try:
        return str(ip_address(value))
    except (ValueError, TypeError):
        return None


def admin_lockout_response(request, response=None, credentials=None, **kwargs):
    response = render(
        request,
        "admin/login_locked.html",
        {
            **admin.site.each_context(request),
            "title": "Acceso temporalmente bloqueado",
            "cooloff_minutes": settings.ADMIN_LOGIN_COOLOFF_MINUTES,
        },
        status=429,
    )
    response["Retry-After"] = str(settings.ADMIN_LOGIN_COOLOFF_MINUTES * 60)
    response["Cache-Control"] = "no-store, private"
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response
