from django.http import Http404
from django.shortcuts import render

from apps.blog.selectors import (
    get_published_blog_post_by_slug,
    get_published_blog_posts,
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
    }

    return render(request, "blog/detail.html", context)
