from django.db import models

from apps.common.models import BaseModel
from apps.common.validators import (
    validate_file_size,
    validate_image_extension,
    validate_safe_link,
)


class SiteConfiguration(BaseModel):
    featured_business = models.ForeignKey(
        "businesses.Business",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="featured_site_configurations",
        verbose_name="Línea destacada del Home",
    )
    site_name = models.CharField(max_length=120, default="Pámi", verbose_name="Nombre del sitio")
    slogan = models.CharField(max_length=180, default="Donde encuentras todo para ti", verbose_name="Eslogan")
    description = models.TextField(blank=True, verbose_name="Descripción")

    email = models.EmailField(blank=True, verbose_name="Correo")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Teléfono")
    whatsapp = models.CharField(max_length=30, blank=True, verbose_name="WhatsApp")
    address = models.CharField(max_length=255, blank=True, verbose_name="Dirección")

    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        validators=(validate_file_size, validate_image_extension),
        verbose_name="Logo",
    )
    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        validators=(validate_file_size, validate_image_extension),
        verbose_name="Favicon",
    )

    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    tiktok_url = models.URLField(blank=True, verbose_name="TikTok")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")

    seo_title = models.CharField(max_length=180, blank=True, verbose_name="Título SEO")
    seo_description = models.CharField(max_length=255, blank=True, verbose_name="Descripción SEO")

    maintenance_mode = models.BooleanField(default=False, verbose_name="Modo mantenimiento")

    hero_title = models.CharField(
        max_length=180,
        default="Todo lo que tu empresa necesita, en un solo lugar.",
        verbose_name="Título del Hero",
    )

    hero_description = models.TextField(
        blank=True,
        default="Confecciones, papelería, tecnología y más, con soluciones para personas, empresas e instituciones.",
        verbose_name="Descripción del Hero",
    )

    hero_primary_button_text = models.CharField(
        max_length=80,
        default="Explorar catálogo",
        verbose_name="Texto botón principal",
    )

    hero_primary_button_url = models.CharField(
        max_length=255,
        default="/catalogo/",
        validators=(validate_safe_link,),
        verbose_name="URL botón principal",
    )

    hero_secondary_button_text = models.CharField(
        max_length=80,
        default="Contáctanos",
        verbose_name="Texto botón secundario",
    )

    hero_secondary_button_url = models.CharField(
        max_length=255,
        default="/contacto/",
        validators=(validate_safe_link,),
        verbose_name="URL botón secundario",
    )

    hero_image = models.ImageField(
        upload_to="site/hero/",
        blank=True,
        null=True,
        validators=(validate_file_size, validate_image_extension),
        verbose_name="Imagen del Hero",
    )

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return self.site_name


class NavigationItem(BaseModel):
    label = models.CharField(max_length=80, verbose_name="Etiqueta")
    url = models.CharField(
        max_length=255,
        validators=(validate_safe_link,),
        verbose_name="URL",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    open_in_new_tab = models.BooleanField(default=False, verbose_name="Abrir en nueva pestaña")

    class Meta:
        verbose_name = "Elemento de navegación"
        verbose_name_plural = "Elementos de navegación"
        ordering = ("order", "label")

    def __str__(self):
        return self.label
