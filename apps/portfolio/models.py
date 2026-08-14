from django.db import models
from django.utils.text import slugify

from apps.businesses.models import Business
from apps.common.models import BaseModel


class PortfolioProject(BaseModel):
    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name="portfolio_projects",
        verbose_name="Línea de negocio",
    )
    title = models.CharField(max_length=150, verbose_name="Título")
    slug = models.SlugField(max_length=170, verbose_name="Slug")
    short_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción corta")
    description = models.TextField(blank=True, verbose_name="Descripción")
    image = models.ImageField(upload_to="portfolio/projects/", blank=True, null=True, verbose_name="Imagen")

    client_name = models.CharField(max_length=120, blank=True, verbose_name="Cliente")
    project_date = models.DateField(blank=True, null=True, verbose_name="Fecha del proyecto")

    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_published = models.BooleanField(default=True, verbose_name="Publicado")

    seo_title = models.CharField(max_length=180, blank=True, verbose_name="Título SEO")
    seo_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción SEO")

    class Meta:
        verbose_name = "Proyecto de portafolio"
        verbose_name_plural = "Proyectos de portafolio"
        ordering = ("business", "order", "title")
        constraints = [
            models.UniqueConstraint(
                fields=["business", "slug"],
                name="unique_portfolio_project_slug_per_business",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title