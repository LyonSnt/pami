from apps.site.models import SiteConfiguration


def get_or_create_site_configuration():
    configuration = SiteConfiguration.objects.order_by("created_at").first()

    if configuration:
        return configuration

    return SiteConfiguration.objects.create(
        site_name="Pámi",
        slogan="Donde encuentras todo para ti",
    )


def update_site_configuration(configuration, **data):
    for field, value in data.items():
        setattr(configuration, field, value)

    configuration.save()
    return configuration
