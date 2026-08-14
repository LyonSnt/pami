from django.shortcuts import get_object_or_404, render

from apps.businesses.selectors import get_published_businesses
from apps.catalog.selectors import (
    get_published_products,
    get_published_products_by_business,
)

from django.urls import reverse


def product_list(request):
    products = get_published_products()

    context = {
        "products": products,
    }

    return render(request, "catalog/list.html", context)


def product_business_list(request, business_slug):
    business = get_object_or_404(
        get_published_businesses(),
        slug=business_slug,
    )
    products = get_published_products_by_business(business)

    context = {
        "business": business,
        "products": products,
    }

    return render(request, "catalog/business_list.html", context)


def product_detail(request, business_slug, product_slug):
    business = get_object_or_404(
        get_published_businesses(),
        slug=business_slug,
    )
    product = get_object_or_404(
        get_published_products_by_business(business),
        slug=product_slug,
    )

    context = {
        "business": business,
        "product": product,
        "breadcrumbs": [
            {
                "label": "Catálogo",
                "url": reverse("catalog:list"),
            },
            {
                "label": business.name,
                "url": reverse(
                    "catalog:business_list",
                    kwargs={"business_slug": business.slug},
                ),
            },
            {
                "label": product.name,
            },
        ],
    }

    return render(request, "catalog/detail.html", context)
