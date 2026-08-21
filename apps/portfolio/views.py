from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.businesses.selectors import get_published_businesses
from apps.contact.services.links import build_contact_url
from apps.portfolio.selectors import (
    get_published_portfolio_projects,
    get_published_portfolio_projects_by_business,
)


def portfolio_project_list(request):
    projects = get_published_portfolio_projects()

    context = {
        "projects": projects,
    }

    return render(request, "portfolio/list.html", context)


def portfolio_project_business_list(request, business_slug):
    business = get_object_or_404(
        get_published_businesses(),
        slug=business_slug,
    )
    projects = get_published_portfolio_projects_by_business(business)

    context = {
        "business": business,
        "projects": projects,
    }

    return render(request, "portfolio/business_list.html", context)


def portfolio_project_detail(request, business_slug, project_slug):
    business = get_object_or_404(
        get_published_businesses(),
        slug=business_slug,
    )
    project = get_object_or_404(
        get_published_portfolio_projects_by_business(business),
        slug=project_slug,
    )

    context = {
        "business": business,
        "project": project,
        "contact_url": build_contact_url(
            business=business,
            subject=f"Consulta sobre {project.title}",
        ),
        "breadcrumbs": [
            {"label": "Portafolio", "url": reverse("portfolio:list")},
            {
                "label": business.name,
                "url": reverse("portfolio:business_list", args=[business.slug]),
            },
            {"label": project.title, "url": None},
        ],
    }

    return render(request, "portfolio/detail.html", context)
