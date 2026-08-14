from django.db import models


class PublishStatus(models.TextChoices):
    DRAFT = "draft", "Borrador"
    PUBLISHED = "published", "Publicado"
    HIDDEN = "hidden", "Oculto"
    ARCHIVED = "archived", "Archivado"


class PublishableMixin(models.Model):
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
        verbose_name="Estado",
    )

    class Meta:
        abstract = True