from django.db import migrations


def preserve_featured_products(apps, schema_editor):
    Business = apps.get_model("businesses", "Business")
    Product = apps.get_model("catalog", "Product")
    database = schema_editor.connection.alias
    business_ids = Business.objects.using(database).filter(
        is_active=True, is_published=True,
    ).values_list("pk", flat=True)
    for business_id in business_ids.iterator():
        product_ids = list(
            Product.objects.using(database).filter(
                business_id=business_id, is_active=True, is_published=True,
            ).order_by("order", "name", "pk").values_list("pk", flat=True)[:2]
        )
        Product.objects.using(database).filter(pk__in=product_ids).update(is_featured=True)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0005_product_featured")]
    operations = [
        migrations.RunPython(preserve_featured_products, migrations.RunPython.noop),
    ]
