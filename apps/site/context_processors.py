from urllib.parse import urlsplit

from apps.site.selectors import (
    get_active_navigation_items,
    get_request_site_configuration,
    is_public_module_enabled,
)
from apps.site.seo import (
    build_absolute_image_url,
    build_organization_structured_data,
)


def site_configuration(request):
    configuration = get_request_site_configuration(request)
    module_visibility = {
        module_name: is_public_module_enabled(configuration, module_name)
        for module_name in ("catalog", "portfolio", "blog", "contact")
    }
    social_image_url = (
        build_absolute_image_url(request, configuration.hero_image)
        if configuration
        else ""
    )

    current_path = request.path_info
    navigation_items = [
        item
        for item in get_active_navigation_items()
        if _navigation_item_is_available(item.url, module_visibility)
    ]
    for item in navigation_items:
        item.is_current = _is_current_internal_path(current_path, item.url)

    return {
        "site_configuration": configuration,
        "navigation_items": navigation_items,
        "home_is_current": current_path == "/",
        "search_is_current": _is_current_internal_path(current_path, "/buscar/"),
        "contact_is_current": _is_current_internal_path(current_path, "/contacto/"),
        "catalog_enabled": module_visibility["catalog"],
        "portfolio_enabled": module_visibility["portfolio"],
        "blog_enabled": module_visibility["blog"],
        "contact_enabled": module_visibility["contact"],
        "show_hero_primary_button": _hero_button_is_available(
            configuration,
            "hero_primary_button_text",
            "hero_primary_button_url",
            module_visibility,
        ),
        "show_hero_secondary_button": _hero_secondary_button_is_available(
            configuration,
            module_visibility,
        ),
        "canonical_url": request.build_absolute_uri(request.path),
        "social_image_url": social_image_url,
        "organization_structured_data": build_organization_structured_data(
            request,
            configuration,
        ),
    }


def _navigation_item_is_available(navigation_url, module_visibility):
    return _url_is_available(navigation_url, module_visibility)


def _url_is_available(url, module_visibility):
    parsed_path = urlsplit(url).path
    module_paths = {
        "/catalogo/": "catalog",
        "/negocios/": "catalog",
        "/portafolio/": "portfolio",
        "/blog/": "blog",
        "/contacto/": "contact",
    }
    for path_prefix, module_name in module_paths.items():
        if parsed_path.startswith(path_prefix):
            return module_visibility[module_name]
    return True


def _hero_secondary_button_is_available(configuration, module_visibility):
    return _hero_button_is_available(
        configuration,
        "hero_secondary_button_text",
        "hero_secondary_button_url",
        module_visibility,
    )


def _hero_button_is_available(
    configuration,
    text_field,
    url_field,
    module_visibility,
):
    if configuration is None or not getattr(configuration, text_field):
        return False
    return _url_is_available(getattr(configuration, url_field), module_visibility)


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
