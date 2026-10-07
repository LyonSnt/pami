from django.db import migrations


def initialize_editorial_texts(apps, schema_editor):
    Business = apps.get_model("businesses", "Business")
    texts = {
        "creaciones": ("Prendas destacadas", "Conoce nuestras prendas."),
        "papeleria": (
            "Productos y servicios destacados",
            "Consulta nuestros productos y servicios de papelería.",
        ),
        "soluciones-digitales": (
            "Sistemas y servicios destacados",
            "Conoce nuestros sistemas y servicios digitales.",
        ),
    }
    for slug, (title, intro) in texts.items():
        businesses = Business.objects.using(schema_editor.connection.alias).filter(slug=slug)
        businesses.filter(featured_title="").update(featured_title=title)
        businesses.filter(catalog_intro="").update(catalog_intro=intro)


class Migration(migrations.Migration):
    dependencies = [("businesses", "0003_business_editorial_texts")]
    operations = [
        migrations.RunPython(initialize_editorial_texts, migrations.RunPython.noop),
    ]
