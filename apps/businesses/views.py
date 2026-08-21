from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.blog.selectors import get_published_blog_posts_by_business
from apps.businesses.selectors import get_published_businesses
from apps.catalog.selectors import get_published_products_by_business
from apps.contact.services.links import build_contact_url
from apps.portfolio.selectors import get_published_portfolio_projects_by_business


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
    products = get_published_products_by_business(business)[:2]
    projects = get_published_portfolio_projects_by_business(business)[:2]
    posts = get_published_blog_posts_by_business(business)[:2]

    context = {
        "business": business,
        "products": products,
        "projects": projects,
        "posts": posts,
        "contact_url": build_contact_url(
            business=business,
            subject=f"Consulta sobre {business.name}",
        ),
        "breadcrumbs": [
            {
                "label": "Líneas de negocio",
                "url": reverse("businesses:list"),
            },
            {"label": business.name},
        ],
    }

    return render(request, "businesses/detail.html", context)
