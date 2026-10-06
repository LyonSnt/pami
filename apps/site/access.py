from django.http import Http404

from apps.site.selectors import request_module_is_enabled


class PublicModuleDisabled(Http404):
    pass


def require_public_module(request, module_name):
    if not request_module_is_enabled(request, module_name):
        raise PublicModuleDisabled
