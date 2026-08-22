from django.db import models
from django.utils.text import slugify

from apps.common.images import responsive_image_spec
from apps.common.models import BaseModel
from apps.common.validators import validate_file_size, validate_image_extension


class Business(BaseModel):
    image_card_small = responsive_image_spec(width=320, height=240)
    image_card = responsive_image_spec(width=640, height=480)
    image_detail = responsive_image_spec(width=1200, height=675)

    name = models.CharField(max_length=120, verbose_name="Nombre")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Slug")
    short_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción corta")
    description = models.TextField(blank=True, verbose_name="Descripción")

    image = models.ImageField(
        upload_to="businesses/",
        blank=True,
        null=True,
        validators=(validate_file_size, validate_image_extension),
        verbose_name="Imagen",
    )
    icon = models.CharField(max_length=80, blank=True, verbose_name="Ícono")

    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_published = models.BooleanField(default=True, verbose_name="Publicado")

    seo_title = models.CharField(max_length=180, blank=True, verbose_name="Título SEO")
    seo_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción SEO")

    class Meta:
        verbose_name = "Línea de negocio"
        verbose_name_plural = "Líneas de negocio"
        ordering = ("order", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
