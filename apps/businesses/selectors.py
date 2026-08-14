from apps.businesses.models import Business


def get_businesses():
    return Business.objects.all()


def get_published_businesses():
    return Business.objects.filter(is_active=True, is_published=True)


def get_business_by_slug(slug):
    return Business.objects.filter(slug=slug).first()
