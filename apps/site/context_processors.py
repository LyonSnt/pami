from urllib.parse import urlsplit

from apps.site.selectors import (
    get_active_navigation_items,
    get_public_site_configuration,
)
from apps.site.seo import (
    build_absolute_image_url,
    build_organization_structured_data,
)


def site_configuration(request):
    if hasattr(request, "_site_configuration"):
        configuration = request._site_configuration
    else:
        configuration = get_public_site_configuration()
        request._site_configuration = configuration
    social_image_url = (
        build_absolute_image_url(request, configuration.hero_image)
        if configuration
        else ""
    )

    current_path = request.path_info
    navigation_items = list(get_active_navigation_items())
    for item in navigation_items:
        item.is_current = _is_current_internal_path(current_path, item.url)

    return {
        "site_configuration": configuration,
        "navigation_items": navigation_items,
        "home_is_current": current_path == "/",
        "search_is_current": _is_current_internal_path(current_path, "/buscar/"),
        "contact_is_current": _is_current_internal_path(current_path, "/contacto/"),
        "canonical_url": request.build_absolute_uri(request.path),
        "social_image_url": social_image_url,
        "organization_structured_data": build_organization_structured_data(
            request,
            configuration,
        ),
    }


def _is_current_internal_path(current_path, navigation_url):
    parsed_url = urlsplit(navigation_url)
    if parsed_url.scheme or parsed_url.netloc or not parsed_url.path.startswith("/"):
        return False

    navigation_path = parsed_url.path
    if navigation_path == "/":
        return current_path == "/"

    normalized_navigation_path = f"{navigation_path.rstrip('/')}/"
    normalized_current_path = f"{current_path.rstrip('/')}/"
    return normalized_current_path.startswith(normalized_navigation_path)
