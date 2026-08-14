from apps.site.selectors import (
    get_active_navigation_items,
    get_public_site_configuration,
)


def site_configuration(request):
    return {
        "site_configuration": get_public_site_configuration(),
        "navigation_items": get_active_navigation_items(),
    }
