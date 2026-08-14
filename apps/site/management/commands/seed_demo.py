from decimal import Decimal

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
        self.create_site_configuration(businesses["confecciones"])
        self.create_navigation()
        self.create_products(businesses)
        self.create_projects(businesses)
        self.create_posts(businesses)

        self.stdout.write(self.style.SUCCESS("Datos demo creados correctamente."))

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
            return

        SiteConfiguration.objects.create(**data)

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

        return businesses

    def create_products(self, businesses):
        data = [
            ("confecciones", "Chaquetas", "chaquetas", "Chaquetas cómodas y versátiles para diferentes estilos.", "45.00", 1),
            ("confecciones", "Buzos", "buzos", "Buzos pensados para brindar comodidad todos los días.", "30.00", 2),
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

        for business_slug, name, slug, description, price, order in data:
            Product.objects.update_or_create(
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

    def create_projects(self, businesses):
        data = [
            ("confecciones", "Colección inicial de chaquetas", "coleccion-inicial-chaquetas", "Confección de una colección demostrativa de chaquetas.", "Pámi"),
            ("confecciones", "Colección inicial de buzos", "coleccion-inicial-buzos", "Confección de una colección demostrativa de buzos.", "Pámi"),
        ]

        PortfolioProject.objects.filter(
            slug__in=(
                "uniformes-equipo-comercial",
                "imagen-impresa-evento",
                "portal-web-institucional",
            ),
        ).update(is_published=False)

        for business_slug, title, slug, description, client_name in data:
            PortfolioProject.objects.update_or_create(
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

    def create_posts(self, businesses):
        data = [
            ("confecciones", "Cómo elegir una chaqueta para tu estilo", "elegir-chaqueta-para-tu-estilo"),
            ("confecciones", "Ideas para combinar tus buzos", "ideas-combinar-buzos"),
        ]

        BlogPost.objects.filter(
            slug__in=(
                "negocio-necesita-pagina-web",
                "ventajas-uniformes-corporativos",
                "materiales-oficina-organizada",
            ),
        ).update(is_published=False)

        for business_slug, title, slug in data:
            BlogPost.objects.update_or_create(
                slug=slug,
                defaults={
                    "business": businesses[business_slug],
                    "title": title,
                    "excerpt": "Artículo demo para validar el diseño del blog.",
                    "content": "Este es un contenido de demostración para revisar cómo se visualiza una publicación dentro del portal Pámi.",
                    "is_published": True,
                    "published_at": timezone.now(),
                    "seo_title": title,
                    "seo_description": "Contenido demo de Pámi.",
                },
            )
