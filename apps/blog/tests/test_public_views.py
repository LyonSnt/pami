from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business


class BlogPublicViewTests(TestCase):
    def test_empty_list_uses_full_width_empty_state(self):
        response = self.client.get(reverse("blog:list"))

        self.assertContains(response, "col-span-full")
        self.assertContains(response, "No hay publicaciones disponibles")

    def test_detail_returns_404_for_future_post(self):
        post = BlogPost.objects.create(
            title="Artículo futuro",
            slug="articulo-futuro",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now() + timedelta(days=1),
        )

        response = self.client.get(
            reverse("blog:detail", kwargs={"slug": post.slug})
        )

        self.assertEqual(response.status_code, 404)

    def test_detail_returns_404_for_inactive_post(self):
        post = BlogPost.objects.create(
            title="Artículo inactivo",
            slug="articulo-inactivo",
            content="Contenido",
            is_active=False,
            is_published=True,
            published_at=timezone.now(),
        )

        response = self.client.get(
            reverse("blog:detail", kwargs={"slug": post.slug})
        )

        self.assertEqual(response.status_code, 404)

    def test_detail_returns_404_when_related_business_is_unpublished(self):
        business = Business.objects.create(
            name="Negocio no publicado",
            slug="negocio-no-publicado",
            is_active=True,
            is_published=False,
        )
        post = BlogPost.objects.create(
            business=business,
            title="Artículo oculto",
            slug="articulo-oculto",
            content="Contenido",
            is_active=True,
            is_published=True,
            published_at=timezone.now(),
        )

        response = self.client.get(
            reverse("blog:detail", kwargs={"slug": post.slug})
        )

        self.assertEqual(response.status_code, 404)
