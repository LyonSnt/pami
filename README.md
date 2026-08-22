# Pámi

Portal público y CMS desarrollado con Django para administrar la marca Pámi y sus líneas de negocio. La presentación editorial actual está enfocada en Confecciones, con Chaquetas y Buzos, bajo el eslogan oficial **“Donde encuentras todo para ti”**.

## Funcionalidades

- Home administrable y responsive.
- Líneas de negocio, catálogo, portafolio y Blog.
- Buscador público con reglas de publicación.
- Formulario de contacto protegido y auditable.
- Roles administrativos para contenido y contacto.
- Modo mantenimiento y páginas de error personalizadas.
- SEO técnico, sitemap, Open Graph, Twitter Cards y JSON-LD.
- Navegación accesible y visor de imágenes en páginas de detalle.

## Tecnologías

- Python 3.12 y Django 5.1.
- PostgreSQL 17.
- Docker Compose.
- Tailwind CSS v4.
- Gunicorn para producción.

## Requisitos

- Docker y Docker Compose.
- Git.

No se requiere instalar Python, PostgreSQL ni Node.js directamente en el equipo.

## Desarrollo local

1. Crear el archivo de entorno a partir de `.env.example`.
2. Sustituir los valores demostrativos de las credenciales locales.
3. Construir e iniciar los servicios:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

4. Cargar el contenido demostrativo en otra terminal:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py seed_demo
```

El portal queda disponible en `http://localhost:8025/` y el administrador en `http://localhost:8025/admin/`, salvo que se modifique `WEB_PORT`.

## Comandos de calidad

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py check
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py makemigrations --check --dry-run
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py test
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm tailwind npm run tailwind
```

La suite estable contiene 105 pruebas.

## Roles administrativos

Los grupos oficiales se crean o actualizan de forma idempotente:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py setup_admin_roles
```

- `Editor de contenido`: gestiona configuración y contenido editorial.
- `Gestor de contacto`: consulta mensajes y administra sus estados.
- El superusuario conserva usuarios, permisos y auditoría.

## Producción

La configuración productiva utiliza `.env.production.example`, `docker-compose.prod.yml` y la imagen multietapa del proyecto. Las instrucciones completas están en [docs/despliegue.md](docs/despliegue.md).

Nunca se deben versionar `.env`, archivos media, copias de base de datos ni `deploy-data/`.

## Documentación

- [Estado actual](docs/estado_actual.md)
- [Próximo paso](docs/proximo_paso.md)
- [Arquitectura](docs/arquitectura.md)
- [Convenciones](docs/convenciones.md)
- [Design System](docs/design-system/README.md)
- [Despliegue](docs/despliegue.md)

## Estado

Versión candidata estable `1.0.0`. El despliegue, dominio y TLS dependen de cada entorno.
