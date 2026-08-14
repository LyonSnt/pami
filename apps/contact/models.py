from django.db import models

from apps.businesses.models import Business
from apps.common.models import BaseModel


class ContactMessage(BaseModel):
    class Status(models.TextChoices):
        NEW = "new", "Nuevo"
        IN_REVIEW = "in_review", "En revisión"
        RESPONDED = "responded", "Respondido"
        CLOSED = "closed", "Cerrado"

    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name="contact_messages",
        blank=True,
        null=True,
        verbose_name="Línea de negocio",
    )
    name = models.CharField(max_length=120, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Teléfono")
    subject = models.CharField(max_length=160, verbose_name="Asunto")
    message = models.TextField(verbose_name="Mensaje")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Estado",
    )
    responded_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de respuesta")

    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} - {self.subject}"