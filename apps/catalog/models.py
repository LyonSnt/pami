from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.text import slugify

from apps.businesses.models import Business
from apps.common.images import responsive_image_spec
from apps.common.models import BaseModel
from apps.common.validators import validate_file_size, validate_image_extension


class Product(BaseModel):
    image_card_small = responsive_image_spec(width=320, height=240)
    image_card = responsive_image_spec(width=640, height=480)
    image_detail = responsive_image_spec(width=960, height=720)

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
    image = models.ImageField(
        upload_to="catalog/products/",
        blank=True,
        null=True,
        validators=(validate_file_size, validate_image_extension),
        verbose_name="Imagen",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=(MinValueValidator(Decimal("0.01")),),
        verbose_name="Precio",
    )
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
            ),
            models.CheckConstraint(
                condition=Q(price__isnull=True) | Q(price__gt=0),
                name="product_price_is_null_or_positive",
            ),
            models.CheckConstraint(
                condition=Q(show_price=False) | Q(price__isnull=False),
                name="product_visible_price_has_value",
            ),
        ]

    def clean(self):
        super().clean()
        if self.show_price and self.price is None:
            raise ValidationError(
                {"price": "Ingresa un precio para poder mostrarlo."}
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
