from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.urls import reverse

from apps.blog.selectors import get_published_blog_posts
from apps.businesses.selectors import get_published_businesses
from apps.catalog.selectors import get_published_products
from apps.portfolio.selectors import get_published_portfolio_projects


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return (
            "site:home",
            "businesses:list",
            "catalog:list",
            "portfolio:list",
            "blog:list",
            "contact:form",
        )

    def location(self, item):
        return reverse(item)


class BusinessSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return get_published_businesses()

    def location(self, business):
        return reverse("businesses:detail", args=[business.slug])

    def lastmod(self, business):
        return business.updated_at


class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return get_published_products()

    def location(self, product):
        return reverse("catalog:detail", args=[product.business.slug, product.slug])

    def lastmod(self, product):
        return product.updated_at


class PortfolioSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return get_published_portfolio_projects()

    def location(self, project):
        return reverse("portfolio:detail", args=[project.business.slug, project.slug])

    def lastmod(self, project):
        return project.updated_at


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return get_published_blog_posts()

    def location(self, post):
        return reverse("blog:detail", args=[post.slug])

    def lastmod(self, post):
        return post.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "businesses": BusinessSitemap,
    "products": ProductSitemap,
    "portfolio": PortfolioSitemap,
    "blog": BlogSitemap,
}


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    content = "\n".join(
        (
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /contacto/enviado/",
            f"Sitemap: {sitemap_url}",
        )
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
