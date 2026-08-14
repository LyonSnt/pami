from django.shortcuts import render

from apps.businesses.selectors import get_published_businesses
from apps.catalog.selectors import get_published_products_by_business
from apps.portfolio.selectors import get_published_portfolio_projects_by_business
from apps.site.selectors import get_public_site_configuration


def home(request):
    site_configuration = get_public_site_configuration()
    featured_business_id = (
        site_configuration.featured_business_id
        if site_configuration
        else None
    )
    business = (
        get_published_businesses().filter(pk=featured_business_id).first()
        if featured_business_id
        else None
    )
    products = get_published_products_by_business(business)[:2] if business else []
    projects = get_published_portfolio_projects_by_business(business)[:3] if business else []

    context = {
        "site_configuration": site_configuration,
        "business": business,
        "products": products,
        "projects": projects,
    }

    return render(request, "site/home.html", context)
