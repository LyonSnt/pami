from django.shortcuts import get_object_or_404, render

from apps.businesses.selectors import get_published_businesses
from apps.contact.services.links import build_contact_url


def business_list(request):
    businesses = get_published_businesses()

    context = {
        "businesses": businesses,
    }

    return render(request, "businesses/list.html", context)


def business_detail(request, slug):
    business = get_object_or_404(
        get_published_businesses(),
        slug=slug,
    )

    context = {
        "business": business,
        "contact_url": build_contact_url(
            business=business,
            subject=f"Consulta sobre {business.name}",
        ),
    }

    return render(request, "businesses/detail.html", context)
