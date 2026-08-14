from apps.catalog.models import Product


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


def get_product_by_slug(business, slug):
    return (
        Product.objects
        .select_related("business")
        .filter(business=business, slug=slug)
        .first()
    )
