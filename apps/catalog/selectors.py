from apps.catalog.models import Product, ProductFeature, ProductImage
from django.db.models import Prefetch, Q


def get_products():
    return Product.objects.select_related("business").all()


def get_published_products():
    return (
        Product.objects
        .select_related("business")
        .filter(
            is_active=True,
            is_published=True,
            business__is_active=True,
            business__is_published=True,
        )
    )


def get_products_by_business(business):
    return (
        Product.objects
        .select_related("business")
        .filter(business=business)
    )


def get_published_products_by_business(business):
    return (
        Product.objects
        .select_related("business")
        .filter(
            business=business,
            is_active=True,
            is_published=True,
            business__is_active=True,
            business__is_published=True,
        )
    )


def search_published_products(query):
    return get_published_products().filter(
        Q(name__icontains=query)
        | Q(short_description__icontains=query)
        | Q(description__icontains=query)
        | Q(target_audience__icontains=query)
        | Q(additional_information__icontains=query)
        | Q(features__title__icontains=query, features__is_active=True)
        | Q(features__description__icontains=query, features__is_active=True)
        | Q(business__name__icontains=query)
    ).distinct()


def with_public_product_details(queryset):
    return queryset.prefetch_related(
        Prefetch(
            "features",
            queryset=ProductFeature.objects.filter(is_active=True),
            to_attr="public_features",
        ),
        Prefetch(
            "gallery_images",
            queryset=ProductImage.objects.filter(is_active=True),
            to_attr="public_gallery_images",
        ),
    )


def get_product_by_slug(business, slug):
    return (
        Product.objects
        .select_related("business")
        .filter(business=business, slug=slug)
        .first()
    )
