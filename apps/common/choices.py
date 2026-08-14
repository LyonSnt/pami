from django.db import models


class ContactStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    ATTENDED = "attended", "Atendido"
    ARCHIVED = "archived", "Archivado"


class VisibilityStatus(models.TextChoices):
    PUBLIC = "public", "Público"
    PRIVATE = "private", "Privado"