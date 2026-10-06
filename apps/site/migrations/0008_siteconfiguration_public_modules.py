from django.db import migrations, models


def focus_public_portal_on_catalog(apps, schema_editor):
    NavigationItem = apps.get_model("site", "NavigationItem")
    NavigationItem.objects.filter(
        label__in=("Portafolio", "Blog", "Contacto"),
    ).update(is_active=False)


class Migration(migrations.Migration):
    dependencies = [
        ("site", "0007_use_general_catalog_navigation"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="show_blog",
            field=models.BooleanField(default=False, verbose_name="Mostrar blog"),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="show_catalog",
            field=models.BooleanField(default=True, verbose_name="Mostrar catálogo"),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="show_contact",
            field=models.BooleanField(default=False, verbose_name="Mostrar contacto"),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="show_portfolio",
            field=models.BooleanField(default=False, verbose_name="Mostrar portafolio"),
        ),
        migrations.RunPython(
            focus_public_portal_on_catalog,
            migrations.RunPython.noop,
        ),
    ]
