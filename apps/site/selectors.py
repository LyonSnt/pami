from apps.site.models import NavigationItem, SiteConfiguration


def get_site_configuration():
    return SiteConfiguration.objects.order_by("created_at").first()


def get_public_site_configuration():
    return get_site_configuration()


def get_active_navigation_items():
    return NavigationItem.objects.filter(is_active=True)
