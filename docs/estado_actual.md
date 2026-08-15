# Estado actual Pámi

## Resumen

Pámi dispone de una base funcional de CMS y portal público construida con Django, PostgreSQL, Docker Compose y Tailwind CSS v4.

La arquitectura conserva soporte para múltiples líneas de negocio, pero el enfoque editorial público actual está centrado en Confecciones para público general.

La auditoría técnica y los nueve bloques de corrección fueron completados. La validación visual del portal público de Confecciones también fue completada en móvil, tablet y escritorio, incluyendo Home, catálogo, portafolio, blog y contacto. La fase de SEO técnico y contenido SEO esencial está implementada. El buscador real del portal está implementado y aprobado visualmente. El proyecto no tiene cambios de migración pendientes y la suite actual contiene 78 pruebas correctas.

## Infraestructura

- Python 3.12-slim.
- Django 5.1.
- PostgreSQL 17-alpine.
- Docker Compose como entorno oficial.
- Servicios `web`, `db` y `tailwind` en desarrollo.
- PostgreSQL con healthcheck.
- `web` condicionado a una base saludable.
- Puertos externos configurados desde `.env`.
- Node.js y Tailwind aislados en Docker.
- Tailwind CSS v4.3.2 validado.
- `STATIC_URL` y `MEDIA_URL` configuradas como rutas absolutas.
- Media servida por Django únicamente en desarrollo.
- WSGI y ASGI utilizan settings de producción por defecto.

## Backend

Apps implementadas:

- `common`;
- `audit`;
- `accounts`;
- `site`;
- `businesses`;
- `catalog`;
- `portfolio`;
- `blog`;
- `contact`.

Estado funcional:

- Usuario personalizado y perfil automático.
- Singleton administrativo de `SiteConfiguration`.
- Menú dinámico mediante `NavigationItem`.
- Modelos, admins, selectors y services principales implementados.
- Selectors públicos con filtros de actividad, publicación, fecha y línea relacionada.
- Views públicas coordinadas mediante selectors.
- Formulario de contacto creado mediante service.
- Transiciones de mensajes de contacto controladas por services.
- Auditoría activa para operaciones administrativas del CMS y envíos de contacto.
- Registros de auditoría inmutables desde Django Admin.
- Estado activo y publicación gestionables desde los administradores editoriales.
- Configuración única protegida contra eliminación desde Django Admin.
- Imágenes editoriales limitadas a JPG, PNG o WebP y a un máximo de 5 MB.
- Enlaces del Hero y la navegación restringidos a rutas internas, anclas o HTTP/HTTPS.
- Roles administrativos idempotentes para edición de contenido y gestión de contacto.
- Inicios y cierres de sesión registrados en la auditoría.
- Consulta de auditoría y administración de usuarios reservadas al superusuario.
- Modo mantenimiento funcional con respuesta HTTP 503, acceso administrativo y revisión para usuarios staff.
- Precios visibles protegidos mediante validación y restricciones de base de datos.

## Portal público

Páginas disponibles:

- Home;
- negocios;
- catálogo;
- portafolio;
- blog;
- contacto.

Características:

- Template base global.
- Header y footer reutilizables.
- Navegación dinámica para escritorio y móvil.
- Hero administrable desde `SiteConfiguration`.
- Línea destacada del Home seleccionable desde `SiteConfiguration`.
- Home modular.
- Home enfocado en productos y trabajos publicados de Confecciones.
- Imágenes WebP representativas para el Hero, Chaquetas, Buzos y los trabajos destacados.
- Imágenes y contenido representativos para los artículos de Confecciones.
- Breadcrumb accesible.
- Estados vacíos reutilizables.
- CTA reutilizable.
- Formulario de contacto accesible.
- Skip link, foco visible y mensajes con región viva.
- Acciones adaptadas a pantallas estrechas.
- Títulos y descripciones SEO específicos por página.
- Canonical, Open Graph y Twitter Cards en el portal público.
- `robots.txt` y `sitemap.xml` con filtros de publicación vigentes.
- Confirmación de contacto excluida de indexación mediante `noindex, follow`.
- Encabezados principales semánticos y breadcrumbs completos en detalles editoriales.
- Buscador responsive con resultados agrupados de productos, proyectos, artículos y líneas de negocio.
- Búsqueda limitada a contenido activo, publicado y vigente.
- Acceso al buscador desde la navegación de escritorio y móvil.
- Página de resultados excluida de indexación mediante `noindex, follow`.
- Página responsive de mantenimiento excluida de indexación.
- Páginas públicas 404 y 500 con identidad Pámi, acciones de recuperación y exclusión de indexación.
- Respuesta 500 autónoma y sin consultas a base de datos.
- Formulario de contacto protegido mediante honeypot y deduplicación temporal por sesión.
- Notificación de nuevos contactos configurable por correo y tolerante a fallos SMTP.
- Scaffolding vacío eliminado; la estructura de apps conserva solo paquetes obligatorios y módulos con responsabilidad real.
- Configuración global reutilizada dentro de la petición del Home para evitar una consulta duplicada.
- Presupuestos de consultas cubiertos por pruebas para Home y buscador.
- Archivos estáticos versionados por contenido en producción para permitir caché prolongada segura.

## Componentes

Organización oficial:

```text
templates/components/
├── cards/
├── layout/
├── sections/
└── ui/
```

Componentes relevantes:

- `button.html`, con variantes `primary`, `secondary` e `inverse`;
- `empty_state.html`;
- `breadcrumb.html`;
- `card_media.html`;
- `section_title.html`;
- `hero.html`;
- `benefits.html`;
- `call_to_action.html`;
- cards de negocios, productos, proyectos y artículos.

Las cards utilizan imágenes administrables y el icono oficial como fallback decorativo.

El catálogo inicial de Confecciones utiliza `Product` para administrar `Chaquetas` y `Buzos`. No se añadió un modelo de categorías ni se realizaron cambios arquitectónicos o de migraciones para este enfoque.

El Home ya no depende del slug fijo `confecciones`: utiliza la línea destacada configurada en Django Admin para resolver la etiqueta del Hero, los productos y los trabajos. El eslogan oficial `Donde encuentras todo para ti` se presenta junto al logo y se repite en el footer para permanecer visible en móvil, siempre separado del mensaje comercial del Hero.

El comando `seed_demo` es idempotente para este contenido: actualiza la configuración demostrativa, publica Chaquetas y Buzos con orden explícito y despublica únicamente los registros demo anteriores conocidos sin eliminarlos. La base de desarrollo fue cargada con este estado.

El mismo comando completa las imágenes demo aprobadas cuando los campos correspondientes están vacíos. Las imágenes reemplazadas posteriormente desde Django Admin se conservan. Los originales optimizados viven en `static/assets/demo/confecciones/` y el conjunto WebP ocupa menos de 450 KB.

La validación responsive del Home confirmó:

- Hero en proporción panorámica para móvil y tablet, con proporción `4:3` en escritorio;
- eslogan legible en tablet y escritorio y disponible en el footer para móvil;
- productos y proyectos en una cuadrícula equilibrada de dos columnas desde `sm`;
- ausencia de desbordamientos visibles y correcta legibilidad de acciones y tarjetas.

La validación de páginas internas confirmó:

- listados de catálogo, portafolio y blog centrados en cuadrículas de dos columnas;
- detalles de productos y proyectos con imagen e información en una composición responsive;
- detalle editorial del blog con imagen panorámica y ancho de lectura controlado;
- descripciones demo duplicadas eliminadas y contenido representativo cargado mediante `seed_demo`;
- formulario de contacto accesible, selector descriptivo y confirmación anunciada mediante una región de estado;
- footer compacto y ubicado al final de páginas con poco contenido.

## Design System

Definido para:

- marca;
- colores;
- tipografía;
- espaciado;
- componentes;
- layout;
- formularios;
- iconos;
- responsive;
- accesibilidad.

Tokens oficiales de Tailwind CSS v4:

- `primary`: `#E31B23`;
- `primary-hover`: `#C8161D`;
- `font-sans`: Inter.

La interfaz utiliza la paleta `slate` y no conserva usos de `gray-*` ni sustituciones `red-600/red-700` para la identidad institucional.

## Branding

Recursos disponibles en `static/assets/branding/`:

- `logo.svg`;
- `logo-white.svg`;
- `icon.svg`;
- `favicon.svg`.

Los beneficios utilizan iconos SVG accesibles y no símbolos de texto provisionales.

## Calidad

- 78 pruebas ejecutadas correctamente.
- `python manage.py check`: sin problemas.
- `makemigrations --check --dry-run`: sin cambios detectados.
- Los SVG de branding son XML válido.
- Tailwind recompilado después de los cambios visuales.

## Consideraciones de producción

La configuración de producción incluye redirección HTTPS, cookies seguras y HSTS configurables.

Antes de desplegar se debe:

- definir una `SECRET_KEY` larga y aleatoria;
- confirmar si todos los subdominios utilizarán HTTPS antes de activar `SECURE_HSTS_INCLUDE_SUBDOMAINS`;
- confirmar la política de preload antes de activar `SECURE_HSTS_PRELOAD`;
- configurar la entrega de static y media en la infraestructura de producción.

## Estado de reanudación

El buscador real está implementado, validado técnicamente y aprobado visualmente. El primer despliegue en Hetzner fue completado y validado por IP sobre HTTP temporal: Nginx publica el puerto `8025`, Gunicorn permanece en `127.0.0.1:8026`, PostgreSQL no se expone y el contenido demo carga correctamente. `check --deploy` conserva cuatro advertencias esperadas hasta incorporar dominio y HTTPS. La reanudación debe comenzar por rotación de secretos expuestos, revisión de firewall, backups y preparación de TLS.
