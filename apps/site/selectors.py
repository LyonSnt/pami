from apps.site.models import NavigationItem, SiteConfiguration


def get_site_configuration():
    return SiteConfiguration.objects.order_by("created_at").first()


def get_public_site_configuration():
    return get_site_configuration()


def get_request_site_configuration(request):
    if hasattr(request, "_site_configuration"):
        return request._site_configuration

    configuration = get_public_site_configuration()
    request._site_configuration = configuration
    return configuration


def is_public_module_enabled(configuration, module_name):
    if configuration is None:
        return True
    return bool(getattr(configuration, f"show_{module_name}", False))


def request_module_is_enabled(request, module_name):
    return is_public_module_enabled(
        get_request_site_configuration(request),
        module_name,
    )


def get_active_navigation_items():
    return NavigationItem.objects.filter(is_active=True)
