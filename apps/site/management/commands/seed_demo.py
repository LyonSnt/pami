from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.businesses.models import Business
from apps.catalog.models import Product
from apps.portfolio.models import PortfolioProject
from apps.site.models import NavigationItem, SiteConfiguration


class Command(BaseCommand):
    help = "Crea datos demo para Pámi."

    def handle(self, *args, **options):
        businesses = self.create_businesses()
        configuration = self.create_site_configuration(businesses["confecciones"])
        self.set_demo_image(
            configuration,
            "hero_image",
            "pami-confecciones-hero.webp",
            "hero.webp",
        )
        self.create_navigation()
        self.create_products(businesses)
        self.create_projects(businesses)
        self.create_posts(businesses)

        self.stdout.write(self.style.SUCCESS("Datos demo creados correctamente."))

    def set_demo_image(self, instance, field_name, storage_name, asset_name):
        image_field = getattr(instance, field_name)
        if image_field:
            return

        asset_path = (
            Path(settings.BASE_DIR)
            / "static"
            / "assets"
            / "demo"
            / "confecciones"
            / asset_name
        )
        with asset_path.open("rb") as asset_file:
            image_field.save(storage_name, File(asset_file), save=True)

    def create_site_configuration(self, featured_business):
        configuration = SiteConfiguration.objects.first()
        data = {
            "featured_business": featured_business,
            "site_name": "Pámi",
            "slogan": "Donde encuentras todo para ti",
            "description": "Pámi crea prendas cómodas y versátiles para acompañarte todos los días.",
            "email": "contacto@pami.test",
            "phone": "099 999 9999",
            "whatsapp": "099 999 9999",
            "address": "Ecuador",
            "seo_title": "Pámi | Chaquetas y buzos",
            "seo_description": "Descubre chaquetas y buzos confeccionados por Pámi.",
            "hero_title": "Chaquetas y buzos hechos para ti.",
            "hero_description": "Conoce prendas cómodas, versátiles y pensadas para acompañar tu estilo.",
            "hero_primary_button_text": "Ver confecciones",
            "hero_primary_button_url": "/catalogo/confecciones/",
        }

        if configuration:
            for field, value in data.items():
                setattr(configuration, field, value)
            configuration.save(update_fields=(*data.keys(), "updated_at"))
            return configuration

        return SiteConfiguration.objects.create(**data)

    def create_navigation(self):
        NavigationItem.objects.filter(
            label__in=("Negocios", "Catálogo"),
        ).update(is_active=False)

        items = [
            ("Inicio", "/", 1),
            ("Confecciones", "/catalogo/confecciones/", 2),
            ("Portafolio", "/portafolio/", 3),
            ("Blog", "/blog/", 4),
            ("Contacto", "/contacto/", 5),
        ]

        for label, url, order in items:
            NavigationItem.objects.update_or_create(
                label=label,
                defaults={
                    "url": url,
                    "order": order,
                    "is_active": True,
                },
            )

    def create_businesses(self):
        Business.objects.filter(
            slug__in=("papeleria", "tecnologia"),
        ).update(is_published=False)

        data = [
            {
                "name": "Confecciones",
                "slug": "confecciones",
                "short_description": "Chaquetas y buzos para acompañar tu estilo.",
                "description": "Creamos prendas cómodas y versátiles para el público en general.",
                "order": 1,
            },
        ]

        businesses = {}

        for item in data:
            business, _ = Business.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    **item,
                    "is_published": True,
                    "seo_title": item["name"],
                    "seo_description": item["short_description"],
                },
            )
            businesses[item["slug"]] = business
            if item["slug"] == "confecciones":
                self.set_demo_image(
                    business,
                    "image",
                    "pami-confecciones.webp",
                    "hero.webp",
                )

        return businesses

    def create_products(self, businesses):
        data = [
            ("confecciones", "Chaquetas", "chaquetas", "Chaquetas cómodas y versátiles para diferentes estilos.", "45.00", 1, "chaquetas.webp"),
            ("confecciones", "Buzos", "buzos", "Buzos pensados para brindar comodidad todos los días.", "30.00", 2, "buzos.webp"),
        ]

        Product.objects.filter(
            slug__in=(
                "uniformes-corporativos",
                "camisetas-personalizadas",
                "tarjetas-presentacion",
                "material-oficina",
                "pagina-web-corporativa",
                "soporte-tecnico",
            ),
        ).update(is_published=False)

        for business_slug, name, slug, description, price, order, asset_name in data:
            product, _ = Product.objects.update_or_create(
                business=businesses[business_slug],
                slug=slug,
                defaults={
                    "name": name,
                    "short_description": description,
                    "description": description,
                    "price": Decimal(price),
                    "show_price": True,
                    "order": order,
                    "is_published": True,
                    "seo_title": name,
                    "seo_description": description,
                },
            )
            self.set_demo_image(
                product,
                "image",
                f"pami-{slug}.webp",
                asset_name,
            )

    def create_projects(self, businesses):
        data = [
            ("confecciones", "Colección inicial de chaquetas", "coleccion-inicial-chaquetas", "Confección de una colección demostrativa de chaquetas.", "Pámi", "proyecto-chaquetas.webp"),
            ("confecciones", "Colección inicial de buzos", "coleccion-inicial-buzos", "Confección de una colección demostrativa de buzos.", "Pámi", "proyecto-buzos.webp"),
        ]

        PortfolioProject.objects.filter(
            slug__in=(
                "uniformes-equipo-comercial",
                "imagen-impresa-evento",
                "portal-web-institucional",
            ),
        ).update(is_published=False)

        for business_slug, title, slug, description, client_name, asset_name in data:
            project, _ = PortfolioProject.objects.update_or_create(
                business=businesses[business_slug],
                slug=slug,
                defaults={
                    "title": title,
                    "short_description": description,
                    "description": description,
                    "client_name": client_name,
                    "project_date": timezone.now().date(),
                    "is_published": True,
                    "seo_title": title,
                    "seo_description": description,
                },
            )
            self.set_demo_image(
                project,
                "image",
                f"pami-{slug}.webp",
                asset_name,
            )

    def create_posts(self, businesses):
        data = [
            (
                "confecciones",
                "Cómo elegir una chaqueta para tu estilo",
                "elegir-chaqueta-para-tu-estilo",
                "Encuentra una chaqueta cómoda y versátil que se adapte a tu forma de vestir.",
                "Una buena chaqueta debe acompañar tu rutina y combinar con las prendas que ya utilizas. Los tonos neutros son fáciles de integrar y funcionan en diferentes momentos del día.\n\nTambién conviene revisar el ajuste, la movilidad de los brazos y el tipo de tejido. Una prenda cómoda permite añadir capas sin perder libertad de movimiento.\n\nEn Pámi confeccionamos chaquetas pensadas para equilibrar estilo, comodidad y uso cotidiano.",
                "proyecto-chaquetas.webp",
            ),
            (
                "confecciones",
                "Ideas para combinar tus buzos",
                "ideas-combinar-buzos",
                "Descubre formas sencillas de incorporar un buzo cómodo a tus looks diarios.",
                "Los buzos en colores neutros combinan fácilmente con jeans, pantalones deportivos y prendas ligeras. Puedes utilizarlos como pieza principal o añadir una chaqueta cuando necesites una capa adicional.\n\nPara un estilo equilibrado, combina prendas amplias con piezas de corte más definido. Los accesorios sencillos y el calzado adecuado permiten adaptar el mismo buzo a diferentes ocasiones.\n\nLos buzos Pámi están pensados para brindar comodidad sin dejar de lado un estilo versátil y actual.",
                "proyecto-buzos.webp",
            ),
        ]

        BlogPost.objects.filter(
            slug__in=(
                "negocio-necesita-pagina-web",
                "ventajas-uniformes-corporativos",
                "materiales-oficina-organizada",
            ),
        ).update(is_published=False)

        for business_slug, title, slug, excerpt, content, asset_name in data:
            post, _ = BlogPost.objects.update_or_create(
                slug=slug,
                defaults={
                    "business": businesses[business_slug],
                    "title": title,
                    "excerpt": excerpt,
                    "content": content,
                    "is_published": True,
                    "published_at": timezone.now(),
                    "seo_title": title,
                    "seo_description": excerpt,
                },
            )
            self.set_demo_image(
                post,
                "image",
                f"pami-{slug}.webp",
                asset_name,
            )
