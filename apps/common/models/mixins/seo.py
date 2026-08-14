from django.db import models


class SEOModel(models.Model):
    slug = models.SlugField(
        max_length=180,
        unique=True,
        verbose_name="Slug",
    )
    seo_title = models.CharField(
        max_length=180,
        blank=True,
        verbose_name="Título SEO",
    )
    seo_description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Descripción SEO",
    )

    class Meta:
        abstract = True