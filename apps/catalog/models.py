from django.db import models
from django.utils.text import slugify

from apps.businesses.models import Business
from apps.common.models import BaseModel


class Product(BaseModel):
    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Línea de negocio",
    )
    name = models.CharField(max_length=120, verbose_name="Nombre")
    slug = models.SlugField(max_length=140, verbose_name="Slug")
    short_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción corta")
    description = models.TextField(blank=True, verbose_name="Descripción")
    image = models.ImageField(upload_to="catalog/products/", blank=True, null=True, verbose_name="Imagen")

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio")
    show_price = models.BooleanField(default=False, verbose_name="Mostrar precio")

    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_published = models.BooleanField(default=True, verbose_name="Publicado")

    seo_title = models.CharField(max_length=180, blank=True, verbose_name="Título SEO")
    seo_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción SEO")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ("business", "order", "name")
        constraints = [
            models.UniqueConstraint(
                fields=["business", "slug"],
                name="unique_product_slug_per_business",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name