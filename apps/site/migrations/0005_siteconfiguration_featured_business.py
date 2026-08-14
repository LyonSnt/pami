import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("businesses", "0001_initial"),
        ("site", "0004_siteconfiguration_hero_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="featured_business",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="featured_site_configurations",
                to="businesses.business",
                verbose_name="Línea destacada del Home",
            ),
        ),
    ]
