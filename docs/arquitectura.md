# Arquitectura Pámi

Pámi es un portal web/CMS propio para administrar una marca principal con múltiples líneas de negocio.

La arquitectura administra múltiples líneas de negocio. El Home mantiene `Creaciones Hadasha` como línea destacada y compone su presentación mediante la etiqueta independiente `Creaciones` y el título `HADASHA` del Hero. El catálogo público permite navegar de forma independiente por Creaciones Hadasha, Soluciones digitales y cualquier línea futura.

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

La ruta administrativa utiliza `settings.ADMIN_URL_PATH`, configurada desde
`ADMIN_URL_PATH` en el entorno y normalizada como un segmento con barra final.
El valor inicial conserva `/admin/`; al cambiarlo no se registra ni redirige
la ruta anterior. El namespace `admin` se mantiene para resolver los enlaces
internos y la excepción de mantenimiento sigue la ruta configurada.

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

Las líneas como Creaciones Hadasha, Soluciones digitales, Papelería y Calzado no son apps separadas.

Serán registros en el modelo `Business`.

`Business` es el eje del CMS. Las apps `catalog`, `portfolio`, `blog` y `contact` pueden relacionar su contenido con una línea de negocio.

`SiteConfiguration` define qué módulos están disponibles públicamente mediante
`show_catalog`, `show_portfolio`, `show_blog` y `show_contact`. Un módulo
desactivado permanece disponible en Django Admin, pero se excluye del Home,
navegación, buscador y sitemap y sus vistas públicas responden 404. La
configuración inicial expone únicamente el catálogo.

`Chaquetas` y `Buzos` son productos asociados a `Creaciones Hadasha`; `Sistema de gestión de agua` es un producto o servicio asociado a `Soluciones digitales`. El catálogo general muestra únicamente las líneas y cada página interna consulta los productos de la línea elegida, evitando mezclar sectores distintos.

`Product` contiene la información comercial común: estado comercial, precio opcional, público objetivo, información adicional y enlace seguro de demostración. `ProductFeature` administra características ordenables y `ProductImage` una galería ordenable con variantes responsive. Esta composición permite incorporar Papelería, Calzado u otros sectores sin crear modelos exclusivos para cada uno.

No existe `ProductCategory`. Solo deberá incorporarse una taxonomía adicional si una línea alcanza un volumen que necesite subdivisiones y filtros internos; no debe utilizarse para representar las líneas de negocio.

`Business.featured_title` y `Business.catalog_intro` contienen textos editoriales
opcionales para el título de destacados del Home y la introducción del catálogo
de cada línea. Se administran por registro y tienen textos generales de respaldo.
Las plantillas no deducen el tipo de oferta a partir del nombre o slug. Las
migraciones `businesses.0003` y `0004` agregan los campos y completan los textos
vacíos de las líneas conocidas sin crear registros ni modificar sus relaciones.

Las antiguas rutas `/negocios/` se conservan únicamente como redirecciones
permanentes hacia `/catalogo/`. De esta forma se mantienen enlaces históricos
sin duplicar públicamente la presentación de líneas de negocio.

`SiteConfiguration.featured_business` define la línea promocionada en el Home y el Home consulta productos y proyectos de esa misma línea. `SiteConfiguration.hero_label` controla de forma independiente la etiqueta breve del Hero; si queda vacía, se utiliza el nombre de la línea destacada como respaldo. Así, el catálogo puede mostrar `Creaciones Hadasha` mientras el Hero conserva la composición `CREACIONES / HADASHA`. Esta relación se administra desde Django Admin y permite cambiar en el futuro a Papelería, Sistemas de agua u otra línea sin modificar templates ni views. La línea utiliza el slug canónico `creaciones`.

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

El login administrativo utiliza `django-axes` con contadores persistentes en
PostgreSQL y bloqueo temporal por nombre de usuario. El backend de control
precede a `ModelBackend` y el middleware de Axes procesa las respuestas de
bloqueo. Los valores y la recuperación se describen en
[Seguridad del administrador](seguridad_admin.md).

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
