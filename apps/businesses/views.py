from django.shortcuts import get_object_or_404, redirect

from apps.businesses.selectors import get_published_businesses
from apps.site.access import require_public_module


def business_list(request):
    require_public_module(request, "catalog")
    return redirect("catalog:list", permanent=True)


def business_detail(request, slug):
    require_public_module(request, "catalog")
    business = get_object_or_404(
        get_published_businesses(),
        slug=slug,
    )
    return redirect(
        "catalog:business_list",
        business_slug=business.slug,
        permanent=True,
    )
