from django.shortcuts import render

from apps.blog.selectors import get_published_blog_posts
from apps.businesses.selectors import get_published_businesses
from apps.catalog.selectors import get_published_products
from apps.portfolio.selectors import get_published_portfolio_projects
from apps.site.selectors import get_public_site_configuration


def home(request):
    businesses = get_published_businesses()[:3]
    products = get_published_products()[:3]
    projects = get_published_portfolio_projects()[:3]
    posts = get_published_blog_posts()[:3]

    context = {
        "site_configuration": get_public_site_configuration(),
        "businesses": businesses,
        "products": products,
        "projects": projects,
        "posts": posts,
    }

    return render(request, "site/home.html", context)