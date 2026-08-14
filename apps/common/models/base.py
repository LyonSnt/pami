import uuid

from django.db import models

from apps.common.managers import ActiveManager


class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de eliminación")

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        abstract = True