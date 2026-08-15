from apps.businesses.models import Business
from django.db.models import Q


def get_businesses():
    return Business.objects.all()


def get_published_businesses():
    return Business.objects.filter(is_active=True, is_published=True)


def search_published_businesses(query):
    return get_published_businesses().filter(
        Q(name__icontains=query)
        | Q(short_description__icontains=query)
        | Q(description__icontains=query)
    )


def get_business_by_slug(slug):
    return Business.objects.filter(slug=slug).first()
