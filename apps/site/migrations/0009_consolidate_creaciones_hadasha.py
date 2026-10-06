from django.db import migrations, models


def consolidate_creaciones_hadasha(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    Business = apps.get_model("businesses", "Business")
    ContactMessage = apps.get_model("contact", "ContactMessage")
    NavigationItem = apps.get_model("site", "NavigationItem")
    PortfolioProject = apps.get_model("portfolio", "PortfolioProject")
    Product = apps.get_model("catalog", "Product")
    SiteConfiguration = apps.get_model("site", "SiteConfiguration")

    canonical = Business.objects.filter(slug="creaciones").first()
    legacy = Business.objects.filter(slug="confecciones").first()

    if canonical is None and legacy is not None:
        legacy.slug = "creaciones"
        legacy.save(update_fields=("slug",))
        canonical = legacy
        legacy = None

    if canonical is not None:
        canonical.name = "Creaciones"
        canonical.short_description = (
            "Hadasha: creamos tu estilo con chaquetas y buzos cómodos y versátiles."
        )
        canonical.description = (
            "Creamos prendas cómodas y versátiles para acompañar tu estilo."
        )
        canonical.seo_title = "Creaciones Hadasha"
        canonical.seo_description = (
            "Descubre las chaquetas y buzos de Creaciones Hadasha."
        )
        canonical.is_active = True
        canonical.is_published = True
        canonical.save(
            update_fields=(
                "name",
                "short_description",
                "description",
                "seo_title",
                "seo_description",
                "is_active",
                "is_published",
            )
        )

    if canonical is not None and legacy is not None:
        for product in Product.objects.filter(business_id=legacy.pk):
            duplicate = Product.objects.filter(
                business_id=canonical.pk,
                slug=product.slug,
            ).exists()
            if duplicate:
                product.delete()
            else:
                product.business_id = canonical.pk
                product.save(update_fields=("business",))

        for project in PortfolioProject.objects.filter(business_id=legacy.pk):
            duplicate = PortfolioProject.objects.filter(
                business_id=canonical.pk,
                slug=project.slug,
            ).exists()
            if duplicate:
                project.delete()
            else:
                project.business_id = canonical.pk
                project.save(update_fields=("business",))

        BlogPost.objects.filter(business_id=legacy.pk).update(
            business_id=canonical.pk
        )
        ContactMessage.objects.filter(business_id=legacy.pk).update(
            business_id=canonical.pk
        )
        SiteConfiguration.objects.filter(
            featured_business_id=legacy.pk
        ).update(featured_business_id=canonical.pk)
        legacy.delete()

    SiteConfiguration.objects.filter(
        description=(
            "Pámi crea prendas cómodas y versátiles para acompañarte todos los días."
        )
    ).update(
        description=(
            "Pámi reúne productos y servicios de sus diferentes líneas de negocio."
        )
    )
    SiteConfiguration.objects.filter(
        seo_title="Pámi | Chaquetas y buzos"
    ).update(seo_title="Pámi | Creaciones Hadasha")
    SiteConfiguration.objects.filter(
        seo_description="Descubre chaquetas y buzos confeccionados por Pámi."
    ).update(
        seo_description="Descubre las chaquetas y buzos de Creaciones Hadasha."
    )
    SiteConfiguration.objects.filter(
        hero_title="Chaquetas y buzos hechos para ti."
    ).update(hero_title="HADASHA")
    SiteConfiguration.objects.filter(
        hero_description=(
            "Conoce prendas cómodas, versátiles y pensadas para acompañar tu estilo."
        )
    ).update(
        hero_description=(
            "Creamos tu estilo con prendas cómodas, versátiles y pensadas para ti."
        )
    )
    SiteConfiguration.objects.filter(
        hero_primary_button_text="Ver confecciones"
    ).update(hero_primary_button_text="Ver productos")
    SiteConfiguration.objects.filter(
        hero_primary_button_url="/catalogo/confecciones/"
    ).update(hero_primary_button_url="/catalogo/creaciones/")

    NavigationItem.objects.filter(
        url="/catalogo/confecciones/"
    ).update(url="/catalogo/creaciones/")
    NavigationItem.objects.filter(label="Confecciones").update(
        label="Creaciones"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_blogpost_image"),
        ("businesses", "0002_alter_business_image"),
        ("catalog", "0004_product_additional_information_and_more"),
        ("contact", "0001_initial"),
        ("portfolio", "0002_alter_portfolioproject_image"),
        ("site", "0008_siteconfiguration_public_modules"),
    ]

    operations = [
        migrations.AlterField(
            model_name="siteconfiguration",
            name="hero_description",
            field=models.TextField(
                blank=True,
                default=(
                    "Creaciones Hadasha, papelería, tecnología y más, con "
                    "soluciones para personas, empresas e instituciones."
                ),
                verbose_name="Descripción del Hero",
            ),
        ),
        migrations.RunPython(
            consolidate_creaciones_hadasha,
            migrations.RunPython.noop,
        ),
    ]
