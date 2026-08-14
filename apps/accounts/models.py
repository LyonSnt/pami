from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico",
    )
    language = models.CharField(
        max_length=10,
        default="es",
        verbose_name="Idioma",
    )


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Usuario",
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Teléfono",
    )
    timezone = models.CharField(
        max_length=50,
        default="America/Guayaquil",
        verbose_name="Zona horaria",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"Perfil de {self.user}"
