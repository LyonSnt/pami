from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from apps.blog.selectors import (
    get_published_blog_post_by_slug,
    get_published_blog_posts,
)
from apps.site.seo import (
    build_absolute_image_url,
    build_blog_post_structured_data,
)


def blog_post_list(request):
    posts = get_published_blog_posts()

    context = {
        "posts": posts,
    }

    return render(request, "blog/list.html", context)


def blog_post_detail(request, slug):
    post = get_published_blog_post_by_slug(slug)
    if post is None:
        raise Http404

    context = {
        "post": post,
        "page_social_image_url": build_absolute_image_url(request, post.image),
        "page_structured_data": build_blog_post_structured_data(request, post),
        "breadcrumbs": [
            {"label": "Blog", "url": reverse("blog:list")},
            {"label": post.title, "url": None},
        ],
    }

    return render(request, "blog/detail.html", context)
