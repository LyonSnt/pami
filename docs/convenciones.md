# Convenciones Lyon Dev

## Idioma

El código interno se escribe en inglés.

Los textos visibles al usuario se escriben en español.

## Estructura

Las apps viven dentro de `apps/`.

La configuración vive en `config/`.

La documentación vive en `docs/`.

Las herramientas internas viven en `tools/`.

Las plantillas viven en una carpeta global `templates/` en la raíz del proyecto.

Los archivos estáticos viven en `static/`.

## Creación de apps

No se usa `django-admin startapp`.

Todas las apps se crean copiando la plantilla Lyon Dev:

```bash
cp -r tools/generators/app apps/<app_name>
```

Después de copiar una app, siempre se debe ajustar `apps.py`:

```python
from django.apps import AppConfig


class AppNameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.app_name"
```

Luego se registra la app en `LOCAL_APPS` usando su clase `Config`.

## Organización progresiva

Todas las aplicaciones comienzan con una estructura simple.

Mientras una app tenga un solo modelo o pocos modelos estrechamente relacionados, se mantiene un único `models.py`.

Esta misma regla aplica a:

- `admin.py`
- `selectors.py`
- `permissions.py`
- `views.py`

Solo se evoluciona a paquetes cuando exista una necesidad real de organización.

No se introduce complejidad anticipada.

## Modelos

Los modelos base viven en `apps/common`.

Todo modelo común debe heredar de `BaseModel`.

Si necesita eliminación lógica, también hereda de `SoftDeleteModel`.

Los modelos de apps específicas heredan de los modelos base cuando corresponda.

## Views

Las vistas no deben contener lógica de negocio.

Las vistas coordinan entrada, salida, selectors, services y templates.

## Selectors

Las consultas reutilizables o complejas van en `selectors.py`.

Mientras la app sea pequeña, se mantiene un solo `selectors.py`.

Si la app crece, puede evolucionar a un paquete `selectors/`.

Los selectors públicos siempre deben aplicar las reglas de visibilidad completas:

- registro activo;
- registro publicado;
- fecha de publicación válida, cuando exista;
- línea de negocio activa y publicada, cuando corresponda.

## Services

La lógica de creación, actualización, publicación, archivo o eliminación va en `services/`.

La carpeta `services/` existe desde la plantilla Lyon Dev.

Los archivos dentro de `services/` se crean por recurso, no por el nombre completo del modelo ni por acción.

Ejemplos correctos:

```text
services/settings.py
services/business.py
services/product.py
services/project.py
services/post.py
services/message.py
```

Ejemplos incorrectos:

```text
services/business_service.py
services/create_business.py
services/product_services.py
```

## Permissions

Las reglas de permisos van en `permissions.py`.

Mientras la app sea pequeña, se mantiene un único archivo.

## Auditoría

Las operaciones administrativas sobre recursos del CMS reutilizan:

```text
apps/audit/admin_mixins.py
```

Los registros de `AuditLog` son inmutables desde Django Admin.

## Templates

No se debe colocar lógica de negocio en HTML.

Las plantillas del proyecto viven en `templates/`, no dentro de cada app.

Todas las páginas públicas heredan de:

```django
{% extends "base/base.html" %}
```

Los parciales reutilizables del layout viven en `templates/base/` y usan prefijo `_`.

Ejemplos:

```text
_head.html
_header.html
_footer.html
_messages.html
_sidebar.html
_scripts.html
```

La estructura `templates/components/` solo se creará cuando exista repetición real de componentes.

## Docker

El desarrollo se realiza con Docker Compose.

No se usa SQLite.

La base oficial es PostgreSQL.

Todos los comandos de Django se ejecutan mediante Docker Compose.

## Puertos

Los puertos externos se configuran desde `.env`.

Los puertos internos se mantienen estándar:

- Django: 8000
- PostgreSQL: 5432


# Plantillas

Todas las plantillas del proyecto viven en:

templates/

No se crean templates dentro de las apps.

Estructura:

templates/
    base/
    site/
    businesses/
    catalog/
    portfolio/
    blog/
    contact/
    registration/
    admin/

Todas las páginas públicas heredan de:

templates/base/base.html

# Navegación

La navegación principal NO se escribe directamente en HTML.

Se administra mediante:

NavigationItem

y se consume mediante:

navigation_items

desde el Context Processor.

El archivo:

templates/base/_navigation.html

únicamente renderiza los elementos.

# Tailwind CSS

Se utiliza Tailwind CSS v4.

Arquitectura oficial Lyon Dev:

Docker
│
├── web
├── db
└── tailwind

Node.js nunca se instala en el sistema operativo.

La compilación se realiza mediante:

npm run tailwind

Modo desarrollo:

npm run tailwind:watch

Archivo fuente:

static/css/input.css

Archivo generado:

static/css/output.css

Tokens oficiales definidos en `static/css/input.css`:

- `primary`: `#E31B23`;
- `primary-hover`: `#C8161D`;
- `font-sans`: Inter.


## Branding

Los recursos de marca viven en:

static/assets/branding/

Archivos esperados:

- logo.svg
- logo-white.svg
- icon.svg
- favicon.svg

El logo no debe escribirse manualmente en HTML cuando exista recurso gráfico oficial.

## Componentes

Los componentes reutilizables viven en:

templates/components/

Los nombres deben ser descriptivos y evitar abreviaturas.

Las cards reutilizan `components/ui/card_media.html` para imágenes y fallback de marca.

Los enlaces y botones reutilizan `components/ui/button.html` con sus variantes oficiales.

Correcto:

- call_to_action.html
- business_card.html
- product_card.html

Incorrecto:

- cta.html
- btn.html
- card1.html
