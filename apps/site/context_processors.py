from apps.site.selectors import (
    get_active_navigation_items,
    get_public_site_configuration,
)


def site_configuration(request):
    configuration = get_public_site_configuration()
    social_image_url = ""
    if configuration and configuration.hero_image:
        social_image_url = request.build_absolute_uri(configuration.hero_image.url)

    return {
        "site_configuration": configuration,
        "navigation_items": get_active_navigation_items(),
        "canonical_url": request.build_absolute_uri(request.path),
        "social_image_url": social_image_url,
    }
