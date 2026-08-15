from apps.portfolio.models import PortfolioProject
from django.db.models import Q


def get_portfolio_projects():
    return PortfolioProject.objects.select_related("business").all()


def get_published_portfolio_projects():
    return (
        PortfolioProject.objects
        .select_related("business")
        .filter(
            is_active=True,
            is_published=True,
            business__is_active=True,
            business__is_published=True,
        )
    )


def get_portfolio_projects_by_business(business):
    return (
        PortfolioProject.objects
        .select_related("business")
        .filter(business=business)
    )


def get_published_portfolio_projects_by_business(business):
    return (
        PortfolioProject.objects
        .select_related("business")
        .filter(
            business=business,
            is_active=True,
            is_published=True,
            business__is_active=True,
            business__is_published=True,
        )
    )


def search_published_portfolio_projects(query):
    return get_published_portfolio_projects().filter(
        Q(title__icontains=query)
        | Q(short_description__icontains=query)
        | Q(description__icontains=query)
        | Q(client_name__icontains=query)
        | Q(business__name__icontains=query)
    )


def get_portfolio_project_by_slug(business, slug):
    return (
        PortfolioProject.objects
        .select_related("business")
        .filter(business=business, slug=slug)
        .first()
    )
