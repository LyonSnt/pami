from django.db import migrations, models


def separate_hero_label(apps, schema_editor):
    Business = apps.get_model("businesses", "Business")
    SiteConfiguration = apps.get_model("site", "SiteConfiguration")

    Business.objects.filter(slug="creaciones").update(
        name="Creaciones Hadasha",
        short_description=(
            "Creamos tu estilo con chaquetas y buzos cómodos y versátiles."
        ),
        seo_title="Creaciones Hadasha",
        seo_description=(
            "Descubre las chaquetas y buzos de Creaciones Hadasha."
        ),
    )
    SiteConfiguration.objects.filter(
        featured_business__slug="creaciones"
    ).update(hero_label="Creaciones")


def restore_combined_label(apps, schema_editor):
    Business = apps.get_model("businesses", "Business")
    SiteConfiguration = apps.get_model("site", "SiteConfiguration")

    Business.objects.filter(slug="creaciones").update(
        name="Creaciones",
        short_description=(
            "Hadasha: creamos tu estilo con chaquetas y buzos cómodos y versátiles."
        ),
    )
    SiteConfiguration.objects.filter(
        featured_business__slug="creaciones",
        hero_label="Creaciones",
    ).update(hero_label="")


class Migration(migrations.Migration):
    dependencies = [
        ("businesses", "0002_alter_business_image"),
        ("site", "0009_consolidate_creaciones_hadasha"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="hero_label",
            field=models.CharField(
                blank=True,
                default="",
                max_length=80,
                verbose_name="Etiqueta del Hero",
            ),
        ),
        migrations.RunPython(
            separate_hero_label,
            restore_combined_label,
        ),
    ]
