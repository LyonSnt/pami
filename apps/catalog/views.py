from django.shortcuts import get_object_or_404, render

from apps.businesses.selectors import get_published_businesses
from apps.contact.services.links import build_contact_url
from apps.site.seo import (
    build_absolute_image_url,
    build_product_structured_data,
)
from apps.catalog.selectors import (
    get_published_products_by_business,
    with_public_product_details,
)

from django.urls import reverse


def product_list(request):
    businesses = get_published_businesses()

    context = {
        "businesses": businesses,
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
        with_public_product_details(
            get_published_products_by_business(business)
        ),
        slug=product_slug,
    )

    context = {
        "business": business,
        "product": product,
        "contact_url": build_contact_url(
            business=business,
            subject=f"Consulta sobre {product.name}",
        ),
        "page_social_image_url": build_absolute_image_url(request, product.image),
        "page_structured_data": build_product_structured_data(request, product),
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
