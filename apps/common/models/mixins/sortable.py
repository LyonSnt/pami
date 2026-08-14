from django.db import models


class SortableMixin(models.Model):
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
    )

    class Meta:
        abstract = True
        ordering = ["order"]