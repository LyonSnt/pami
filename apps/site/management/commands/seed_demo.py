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
        self.create_site_configuration()
        businesses = self.create_businesses()
        self.create_navigation()
        self.create_products(businesses)
        self.create_projects(businesses)
        self.create_posts(businesses)

        self.stdout.write(self.style.SUCCESS("Datos demo creados correctamente."))

    def create_site_configuration(self):
        configuration = SiteConfiguration.objects.first()

        if not configuration:
            SiteConfiguration.objects.create(
                site_name="Pámi",
                slogan="Soluciones para tu negocio en un solo lugar",
                description="Pámi conecta diferentes líneas de negocio en un portal moderno, organizado y fácil de administrar.",
                email="contacto@pami.test",
                phone="099 999 9999",
                whatsapp="099 999 9999",
                address="Ecuador",
                seo_title="Pámi | Soluciones para tu negocio",
                seo_description="Portal de servicios, productos, proyectos y contenidos de Pámi.",
            )

    def create_navigation(self):
        items = [
            ("Inicio", "/", 1),
            ("Negocios", "/negocios/", 2),
            ("Catálogo", "/catalogo/", 3),
            ("Portafolio", "/portafolio/", 4),
            ("Blog", "/blog/", 5),
            ("Contacto", "/contacto/", 6),
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
        data = [
            {
                "name": "Confecciones",
                "slug": "confecciones",
                "short_description": "Uniformes, prendas personalizadas y soluciones textiles.",
                "description": "Diseñamos y confeccionamos prendas para empresas, instituciones y emprendimientos.",
                "order": 1,
            },
            {
                "name": "Papelería",
                "slug": "papeleria",
                "short_description": "Suministros, impresiones y materiales para oficina.",
                "description": "Ofrecemos productos de papelería, impresión y soluciones para negocios y estudiantes.",
                "order": 2,
            },
            {
                "name": "Tecnología",
                "slug": "tecnologia",
                "short_description": "Soluciones digitales, soporte técnico y desarrollo web.",
                "description": "Ayudamos a negocios a mejorar sus procesos mediante tecnología y herramientas digitales.",
                "order": 3,
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
            ("confecciones", "Uniformes corporativos", "uniformes-corporativos", "Uniformes personalizados para empresas.", "45.00"),
            ("confecciones", "Camisetas personalizadas", "camisetas-personalizadas", "Camisetas con diseño, logo o marca.", "18.00"),
            ("papeleria", "Tarjetas de presentación", "tarjetas-presentacion", "Diseño e impresión de tarjetas profesionales.", "25.00"),
            ("papeleria", "Material de oficina", "material-oficina", "Suministros básicos para empresas y estudiantes.", "12.00"),
            ("tecnologia", "Página web corporativa", "pagina-web-corporativa", "Sitio web moderno para negocios.", "350.00"),
            ("tecnologia", "Soporte técnico", "soporte-tecnico", "Asistencia técnica para equipos y sistemas.", "30.00"),
        ]

        for business_slug, name, slug, description, price in data:
            Product.objects.update_or_create(
                business=businesses[business_slug],
                slug=slug,
                defaults={
                    "name": name,
                    "short_description": description,
                    "description": description,
                    "price": Decimal(price),
                    "show_price": True,
                    "is_published": True,
                    "seo_title": name,
                    "seo_description": description,
                },
            )

    def create_projects(self, businesses):
        data = [
            ("confecciones", "Uniformes para equipo comercial", "uniformes-equipo-comercial", "Producción de uniformes personalizados.", "Empresa Demo"),
            ("papeleria", "Imagen impresa para evento", "imagen-impresa-evento", "Material gráfico e impresión para evento corporativo.", "Evento Demo"),
            ("tecnologia", "Portal web institucional", "portal-web-institucional", "Desarrollo de sitio web administrable.", "Cliente Demo"),
        ]

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
            ("tecnologia", "Por qué tu negocio necesita una página web", "negocio-necesita-pagina-web"),
            ("confecciones", "Ventajas de usar uniformes corporativos", "ventajas-uniformes-corporativos"),
            ("papeleria", "Materiales básicos para una oficina organizada", "materiales-oficina-organizada"),
        ]

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