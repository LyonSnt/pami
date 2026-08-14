from django.db.models import Q
from django.utils import timezone

from apps.blog.models import BlogPost


def get_blog_posts():
    return BlogPost.objects.select_related("business").all()


def get_published_blog_posts():
    return (
        BlogPost.objects
        .select_related("business")
        .filter(
            Q(business__isnull=True)
            | Q(business__is_active=True, business__is_published=True),
            is_active=True,
            is_published=True,
            published_at__lte=timezone.now(),
        )
    )


def get_blog_posts_by_business(business):
    return (
        BlogPost.objects
        .select_related("business")
        .filter(business=business)
    )


def get_published_blog_posts_by_business(business):
    return (
        BlogPost.objects
        .select_related("business")
        .filter(
            business=business,
            is_active=True,
            is_published=True,
            published_at__lte=timezone.now(),
            business__is_active=True,
            business__is_published=True,
        )
    )


def get_blog_post_by_slug(slug):
    return (
        BlogPost.objects
        .select_related("business")
        .filter(slug=slug)
        .first()
    )


def get_published_blog_post_by_slug(slug):
    return (
        BlogPost.objects
        .select_related("business")
        .filter(
            Q(business__isnull=True)
            | Q(business__is_active=True, business__is_published=True),
            slug=slug,
            is_active=True,
            is_published=True,
            published_at__lte=timezone.now(),
        )
        .first()
    )
