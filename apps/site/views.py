from django.shortcuts import render

from apps.blog.selectors import search_published_blog_posts
from apps.businesses.selectors import (
    get_published_businesses,
    search_published_businesses,
)
from apps.catalog.selectors import (
    get_published_products_by_business,
    search_published_products,
)
from apps.portfolio.selectors import (
    get_published_portfolio_projects_by_business,
    search_published_portfolio_projects,
)
from apps.site.forms import SearchForm
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


def search(request):
    form = SearchForm(request.GET)
    query = ""
    businesses = []
    products = []
    projects = []
    posts = []

    if form.is_valid():
        query = form.cleaned_data["q"]

    if query:
        businesses = search_published_businesses(query)[:6]
        products = search_published_products(query)[:6]
        projects = search_published_portfolio_projects(query)[:6]
        posts = search_published_blog_posts(query)[:6]

    result_count = sum(
        len(results)
        for results in (businesses, products, projects, posts)
    )

    context = {
        "form": form,
        "query": query,
        "businesses": businesses,
        "products": products,
        "projects": projects,
        "posts": posts,
        "result_count": result_count,
    }
    return render(request, "site/search.html", context)
