from django.db import migrations


def use_general_catalog_navigation(apps, schema_editor):
    NavigationItem = apps.get_model("site", "NavigationItem")
    existing_catalog = NavigationItem.objects.filter(label="Catálogo").first()
    confections_items = NavigationItem.objects.filter(
        label="Confecciones",
        url="/catalogo/confecciones/",
    ).order_by("order", "pk")

    if existing_catalog:
        existing_catalog.url = "/catalogo/"
        existing_catalog.is_active = True
        existing_catalog.save(update_fields=("url", "is_active", "updated_at"))
        confections_items.update(is_active=False)
        return

    primary_item = confections_items.first()
    if primary_item:
        primary_item.label = "Catálogo"
        primary_item.url = "/catalogo/"
        primary_item.is_active = True
        primary_item.save(
            update_fields=("label", "url", "is_active", "updated_at")
        )
        confections_items.exclude(pk=primary_item.pk).update(is_active=False)


class Migration(migrations.Migration):
    dependencies = [
        ("site", "0006_alter_navigationitem_url_and_more"),
    ]

    operations = [
        migrations.RunPython(
            use_general_catalog_navigation,
            migrations.RunPython.noop,
        ),
    ]
