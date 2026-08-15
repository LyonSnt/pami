from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.businesses.models import Business
from apps.common.models import BaseModel
from apps.common.validators import validate_file_size, validate_image_extension


class BlogPost(BaseModel):
    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name="blog_posts",
        blank=True,
        null=True,
        verbose_name="Línea de negocio",
    )
    title = models.CharField(max_length=160, verbose_name="Título")
    slug = models.SlugField(max_length=180, unique=True, verbose_name="Slug")
    excerpt = models.CharField(max_length=255, blank=True, verbose_name="Resumen")
    content = models.TextField(verbose_name="Contenido")
    image = models.ImageField(
        upload_to="blog/posts/",
        blank=True,
        null=True,
        validators=(validate_file_size, validate_image_extension),
        verbose_name="Imagen",
    )

    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de publicación")
    is_published = models.BooleanField(default=False, verbose_name="Publicado")

    seo_title = models.CharField(max_length=180, blank=True, verbose_name="Título SEO")
    seo_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción SEO")

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.is_published and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
