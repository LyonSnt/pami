from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class AuditLog(TimeStampedModel):
    class Action(models.TextChoices):
        CREATE = "create", "Crear"
        UPDATE = "update", "Actualizar"
        DELETE = "delete", "Eliminar"
        LOGIN = "login", "Inicio de sesión"
        LOGOUT = "logout", "Cierre de sesión"
        OTHER = "other", "Otro"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Usuario",
    )
    action = models.CharField(
        max_length=30,
        choices=Action.choices,
        verbose_name="Acción",
    )
    app_label = models.CharField(max_length=100, verbose_name="App")
    model_name = models.CharField(max_length=100, verbose_name="Modelo")
    object_id = models.CharField(max_length=100, blank=True, verbose_name="ID objeto")
    object_repr = models.CharField(max_length=255, blank=True, verbose_name="Objeto")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    user_agent = models.TextField(blank=True, verbose_name="Navegador")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="Metadata")

    class Meta:
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_action_display()} - {self.object_repr}"


class DatabaseBackup(AuditLog):
    class Meta:
        proxy = True
        verbose_name = "Respaldo de base de datos"
        verbose_name_plural = "Respaldos de base de datos"
