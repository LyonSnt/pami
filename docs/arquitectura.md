# Arquitectura Pámi

Pámi es un portal web/CMS propio para administrar una marca principal con múltiples líneas de negocio.

La arquitectura continúa preparada para múltiples líneas, aunque el enfoque editorial público actual se concentra en `Confecciones`. Esta prioridad no convierte Confecciones en una app independiente ni elimina la capacidad de publicar otras líneas en el futuro.

## Stack

- Python 3.12-slim
- Django
- PostgreSQL 17-alpine
- Docker Compose
- Tailwind CSS v4
- HTMX (planificado, todavía no integrado)
- Pillow

## Estructura base

- `config/`: configuración Django.
- `config/settings/components/`: configuración modular.
- `config/urls/`: separación de URLs por contexto.
- `apps/`: aplicaciones del sistema.
- `templates/`: plantillas HTML globales.
- `static/`: archivos estáticos del proyecto.
- `media/`: archivos subidos.
- `docs/`: documentación.
- `tools/`: herramientas internas Lyon Dev.

## URLs

Las URLs públicas principales se registran en:

- `config/urls/public.py`

Las apps pueden tener su propio `urls.py`, pero la composición pública se controla desde `config/urls/public.py`.

## Templates

Pámi usa una carpeta global de plantillas en la raíz del proyecto:

```text
templates/
├── base/
│   ├── base.html
│   ├── _header.html
│   ├── _navigation.html
│   ├── _footer.html
│   ├── _messages.html
│   ├── _sidebar.html
│   └── _scripts.html
├── components/
│   ├── cards/
│   ├── layout/
│   ├── sections/
│   └── ui/
├── errors/
├── site/
├── businesses/
├── catalog/
├── portfolio/
├── blog/
└── contact/
```

Todas las páginas públicas heredan de:

```django
{% extends "base/base.html" %}
```

Los parciales reutilizables de layout viven en `templates/base/` y usan prefijo `_`.

Los componentes de interfaz reutilizables viven en `templates/components/` y se organizan en:

- `cards/`;
- `layout/`;
- `sections/`;
- `ui/`.

## Decisiones clave

Las líneas como Confecciones, Papelería y Tecnología no serán apps separadas.

Serán registros en el modelo `Business`.

`Business` es el eje del CMS. Las apps `catalog`, `portfolio`, `blog` y `contact` pueden relacionar su contenido con una línea de negocio.

En la etapa actual, `Chaquetas` y `Buzos` son productos asociados al registro `Confecciones`. No se introduce una taxonomía de categorías hasta que existan productos concretos que necesiten agruparse y filtrarse dentro de cada tipo de prenda.

`SiteConfiguration.featured_business` define la línea promocionada en el Home. El Hero utiliza su nombre como etiqueta y el Home consulta productos y proyectos de esa misma línea. Esta relación se administra desde Django Admin y permite cambiar en el futuro de Confecciones a Papelería, Sistemas de agua u otra línea sin modificar templates ni views.

## Apps base del CMS

- `common`: base reutilizable Lyon Dev.
- `audit`: auditoría transversal.
- `accounts`: usuarios y perfiles.
- `site`: configuración general del portal.
- `businesses`: líneas de negocio.
- `catalog`: catálogo informativo.
- `portfolio`: proyectos o trabajos realizados.
- `blog`: publicaciones.
- `contact`: mensajes de contacto.

## Orden de desarrollo

1. Infraestructura
2. `common`
3. `audit`
4. `accounts`
5. `site`
6. `businesses`
7. `catalog`
8. `portfolio`
9. `blog`
10. `contact`
11. Capa pública del portal

## Separación de responsabilidades

- Las views coordinan entrada, salida y templates.
- Las consultas públicas y reutilizables pertenecen a selectors.
- Las mutaciones y transiciones pertenecen a services.
- Los contenidos públicos deben cumplir `is_active`, publicación y, cuando corresponda, fecha de publicación y estado de su línea de negocio.
- Las operaciones administrativas del CMS utilizan `AuditModelAdminMixin` para registrar altas, cambios y eliminaciones.
- Los módulos opcionales (`forms.py`, `signals.py`, `permissions.py`, `choices.py`, entre otros) se crean solo cuando contienen una responsabilidad real; no se conservan archivos vacíos como marcadores.
- Los `__init__.py` de paquetes y migraciones se conservan aunque no exporten contenido.

## Infraestructura

Docker Compose mantiene los servicios `web`, `db` y, en desarrollo, `tailwind`.

PostgreSQL dispone de healthcheck y `web` espera a que la base se encuentre saludable.

Node.js y Tailwind se ejecutan exclusivamente dentro de Docker.

Los puntos de entrada WSGI y ASGI utilizan configuración de producción por defecto. Los comandos de desarrollo ejecutados mediante `manage.py` utilizan `config.settings.dev`.

## Static y media

- `STATIC_URL = "/static/"`.
- `MEDIA_URL = "/media/"`.
- Django sirve media únicamente cuando `DEBUG=True`.
- La entrega de static y media en producción debe quedar a cargo de la infraestructura de despliegue.

## Pruebas

La suite se ejecuta mediante Docker Compose y utiliza una base temporal independiente:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py test
```


## Portal Público

El portal público utiliza la siguiente arquitectura.

Templates
│
├── base
│   ├── base.html
│   ├── _header.html
│   ├── _navigation.html
│   ├── _footer.html
│   └── _messages.html
│
├── site
├── businesses
├── catalog
├── portfolio
├── blog
└── contact

Todas las vistas públicas heredan de:

base/base.html
