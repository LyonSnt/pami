from django.conf import settings
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

from apps.site.access import PublicModuleDisabled
from apps.site.selectors import get_public_site_configuration


class PublicModuleDisabledMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, PublicModuleDisabled):
            return render(request, "404.html", status=404)
        return None


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_exempt_request(request):
            return self.get_response(request)

        configuration = get_public_site_configuration()
        request._site_configuration = configuration

        if configuration and configuration.maintenance_mode:
            return render(
                request,
                "site/maintenance.html",
                {"site_configuration": configuration},
                status=503,
            )

        return self.get_response(request)

    @staticmethod
    def _is_exempt_request(request):
        exempt_prefixes = (
            f"/{settings.ADMIN_URL_PATH}",
            settings.STATIC_URL,
            settings.MEDIA_URL,
        )
        return request.user.is_staff or request.path_info.startswith(exempt_prefixes)
