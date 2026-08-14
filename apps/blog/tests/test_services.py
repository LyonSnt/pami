from django.test import TestCase

from apps.blog.services.post import create_blog_post


class BlogPostServiceTests(TestCase):
    def test_model_sets_slug_and_published_at_when_service_creates_post(self):
        post = create_blog_post(
            title="Artículo nuevo",
            slug="",
            content="Contenido",
            is_published=True,
        )

        self.assertEqual(post.slug, "articulo-nuevo")
        self.assertIsNotNone(post.published_at)
