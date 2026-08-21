import json

from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.templatetags.static import static
from django.urls import reverse

from apps.blog.selectors import get_published_blog_posts
from apps.businesses.selectors import get_published_businesses
from apps.catalog.selectors import get_published_products
from apps.portfolio.selectors import get_published_portfolio_projects


def build_absolute_image_url(request, image):
    return request.build_absolute_uri(image.url) if image else ""


def serialize_structured_data(data):
    serialized = json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return (
        serialized.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def build_organization_structured_data(request, configuration):
    home_url = request.build_absolute_uri(reverse("site:home"))
    organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{home_url}#organization",
        "name": configuration.site_name if configuration else "Pámi",
        "url": home_url,
    }

    if configuration:
        if configuration.description:
            organization["description"] = configuration.description
        organization["logo"] = build_absolute_image_url(
            request,
            configuration.logo,
        ) or request.build_absolute_uri(static("assets/branding/logo.svg"))
        if configuration.email:
            organization["email"] = configuration.email
        if configuration.phone:
            organization["telephone"] = configuration.phone
        if configuration.address:
            organization["address"] = configuration.address
        same_as = [
            url
            for url in (
                configuration.facebook_url,
                configuration.instagram_url,
                configuration.tiktok_url,
                configuration.youtube_url,
                configuration.linkedin_url,
            )
            if url
        ]
        if same_as:
            organization["sameAs"] = same_as
    else:
        organization["logo"] = request.build_absolute_uri(
            static("assets/branding/logo.svg")
        )

    return serialize_structured_data(organization)


def build_product_structured_data(request, product):
    product_url = request.build_absolute_uri(
        reverse("catalog:detail", args=[product.business.slug, product.slug])
    )
    home_url = request.build_absolute_uri(reverse("site:home"))
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "url": product_url,
        "description": product.seo_description
        or product.short_description
        or product.description,
        "category": product.business.name,
        "brand": {"@id": f"{home_url}#organization"},
    }
    image_url = build_absolute_image_url(request, product.image)
    if image_url:
        data["image"] = image_url
    if product.show_price and product.price:
        data["offers"] = {
            "@type": "Offer",
            "url": product_url,
            "priceCurrency": "USD",
            "price": format(product.price, ".2f"),
        }
    return serialize_structured_data(data)


def build_blog_post_structured_data(request, post):
    post_url = request.build_absolute_uri(reverse("blog:detail", args=[post.slug]))
    home_url = request.build_absolute_uri(reverse("site:home"))
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "url": post_url,
        "mainEntityOfPage": post_url,
        "description": post.seo_description or post.excerpt,
        "datePublished": post.published_at.isoformat(),
        "dateModified": post.updated_at.isoformat(),
        "publisher": {"@id": f"{home_url}#organization"},
    }
    image_url = build_absolute_image_url(request, post.image)
    if image_url:
        data["image"] = image_url
    return serialize_structured_data(data)


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
