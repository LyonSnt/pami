# Estado actual Pámi

## Resumen

Pámi dispone de una base funcional de CMS y portal público construida con Django, PostgreSQL, Docker Compose y Tailwind CSS v4.

La arquitectura soporta múltiples líneas de negocio. El Home conserva Creaciones Hadasha como línea destacada y presenta la composición `CREACIONES / HADASHA`, mientras el catálogo general presenta el nombre comercial completo, Soluciones digitales y queda preparado para Papelería, Calzado u otras líneas futuras.

El desarrollo se encuentra funcionalmente concluido como versión candidata estable `1.0.0`. El repositorio dispone de una guía principal de uso y excluye explícitamente datos locales o productivos mediante `.gitignore` y `.dockerignore`.

La auditoría técnica y los nueve bloques de corrección fueron completados. La validación visual del portal público de Creaciones Hadasha también fue completada en móvil, tablet y escritorio. La fase de SEO técnico y contenido SEO esencial está implementada. El buscador real del portal está implementado y aprobado visualmente. Las imágenes de contenido del Home, tarjetas y páginas de detalle cuentan con ampliación accesible y variantes responsive WebP; los originales se reservan para el zoom. Los superusuarios pueden crear y descargar respaldos manuales PostgreSQL auditados desde el administrador. El catálogo genérico admite galerías, características, estado comercial, público objetivo, información adicional y demostraciones opcionales. Portafolio, Blog y Contacto se conservan administrables, pero están desactivados públicamente mientras Pámi se enfoca en el catálogo. La suite actual contiene 131 pruebas correctas.

## Infraestructura

- Python 3.12-slim.
- Django 5.2 LTS.
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
- Cuentas y perfiles diferenciados en Django Admin mediante etiquetas inequívocas.
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
- Productos con estado comercial, público objetivo, información adicional y enlace seguro de demostración.
- Galerías y características ordenables y reutilizables para cualquier línea de negocio.
- Interruptores administrativos independientes para Catálogo, Portafolio, Blog y Contacto.
- Campo `hero_label` para separar la etiqueta promocional del Hero del nombre comercial de la línea destacada.

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
- Estado activo de navegación calculado por ruta, conservado en páginas internas y anunciado mediante `aria-current`.
- Menú móvil con iconos de apertura y cierre, cierre al elegir una opción, pulsar fuera o presionar Escape.
- Página de línea de negocio con imagen, productos, proyectos y artículos relacionados publicados.
- Resumen de línea limitado a dos registros por tipo y protegido mediante presupuesto de consultas.
- Visor modal accesible para ampliar todas las imágenes públicas de contenido.
- Hero administrable desde `SiteConfiguration`.
- Etiqueta breve del Hero administrable de forma independiente al nombre comercial de la línea destacada.
- Línea destacada del Home seleccionable desde `SiteConfiguration`.
- Home modular.
- Home enfocado en productos y trabajos publicados de Creaciones.
- Imágenes WebP representativas para el Hero, Chaquetas, Buzos y los trabajos destacados.
- Imágenes y contenido representativos para los artículos de Creaciones Hadasha.
- Breadcrumb accesible.
- Estados vacíos reutilizables.
- CTA reutilizable.
- Formulario de contacto accesible.
- Skip link, foco visible y mensajes con región viva.
- Acciones adaptadas a pantallas estrechas.
- Títulos y descripciones SEO específicos por página.
- Canonical, Open Graph y Twitter Cards en el portal público.
- Imágenes sociales específicas para Open Graph y Twitter/X, con Hero como respaldo.
- Datos estructurados JSON-LD seguros para la organización, productos y artículos del Blog.
- `robots.txt` y `sitemap.xml` con filtros de publicación vigentes.
- Confirmación de contacto excluida de indexación mediante `noindex, follow`.
- Encabezados principales semánticos y breadcrumbs completos en detalles editoriales.
- Buscador responsive con resultados agrupados de productos, proyectos, artículos y líneas de negocio.
- El catálogo general funciona como selector de líneas y evita mezclar productos de sectores distintos; cada página interna muestra únicamente los productos o servicios de la línea elegida.
- Los módulos desactivados se excluyen de navegación, Home, buscador y sitemap, y sus rutas públicas responden 404 sin eliminar sus datos.
- Los módulos desactivados muestran el 404 institucional incluso en desarrollo; los errores inesperados conservan el diagnóstico técnico cuando `DEBUG=True`.
- Las rutas históricas de Negocios redirigen permanentemente al catálogo para evitar dos recorridos públicos equivalentes.
- Búsqueda de productos por características activas y contenido comercial adicional.
- Búsqueda limitada a contenido activo, publicado y vigente.
- Acceso al buscador desde la navegación de escritorio y móvil.
- Página de resultados excluida de indexación mediante `noindex, follow`.
- Página responsive de mantenimiento excluida de indexación.
- Páginas públicas 404 y 500 con identidad Pámi, acciones de recuperación y exclusión de indexación.
- Respuesta 500 autónoma y sin consultas a base de datos.
- Formulario de contacto protegido mediante honeypot y deduplicación temporal por sesión.
- Solicitudes de información con línea y asunto preseleccionados desde productos, proyectos y líneas de negocio.
- Límite configurable de envíos de contacto por dirección mediante hash temporal en caché.
- Notificación de nuevos contactos configurable por correo y tolerante a fallos SMTP.
- Scaffolding vacío eliminado; la estructura de apps conserva solo paquetes obligatorios y módulos con responsabilidad real.
- Nombre `Pámi` continuo en el SVG del encabezado para evitar separaciones tipográficas en móvil.
- Logo y favicon cargados en la configuración administrativa utilizados por el portal, con los SVG oficiales como respaldo.
- Correo, teléfono, WhatsApp, dirección y redes sociales configurados presentados como enlaces accesibles en el footer, independientemente de que el formulario de contacto esté activo.
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
- `zoomable_media.html`;
- `section_title.html`;
- `hero.html`;
- `benefits.html`;
- `call_to_action.html`;
- cards de negocios, productos, proyectos y artículos.

Las cards utilizan imágenes administrables y el icono oficial como fallback decorativo.

El catálogo utiliza `Business` como línea de negocio y `Product` como producto o servicio. No necesita categorías para incorporar Creaciones Hadasha, Soluciones digitales, Papelería o Calzado. `ProductFeature` y `ProductImage` aportan características y galerías genéricas sin crear modelos exclusivos para cada sector.

El Home utiliza la línea destacada configurada en Django Admin para resolver los productos y los trabajos. La etiqueta breve del Hero se configura por separado y recurre al nombre de la línea solo cuando está vacía. La línea principal usa el nombre `Creaciones Hadasha` y el slug canónico `creaciones`. El eslogan oficial `Donde encuentras todo para ti` se presenta junto al logo y se repite en el footer para permanecer visible en móvil, siempre separado del mensaje comercial del Hero.

El comando `seed_demo` es idempotente para este contenido: actualiza la configuración demostrativa, publica Chaquetas y Buzos con orden explícito y despublica únicamente los registros demo anteriores conocidos sin eliminarlos. La base de desarrollo fue cargada con este estado.

El mismo comando completa las imágenes demo aprobadas cuando los campos correspondientes están vacíos. Las imágenes reemplazadas posteriormente desde Django Admin se conservan. Los originales optimizados viven en `static/assets/demo/creaciones/` y el conjunto WebP ocupa menos de 450 KB.

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
El bloque del Hero presenta los mensajes generales `Cuidamos los detalles`,
`Entrega confiable` y `Atención cercana`, con descripciones breves. Estos textos
están definidos en la plantilla, no se administran desde el CMS y son
independientes de la línea destacada.
Los iconos representan un check, un camión y una burbuja de conversación;
conservan tamaños, colores y fondos consistentes con el Design System.

## Calidad

- 131 pruebas ejecutadas correctamente.
- `python manage.py check`: sin problemas.
- `makemigrations --check --dry-run`: sin cambios detectados.
- Migración `site.0010_separate_hero_label` aplicada y validada en desarrollo.
- Los SVG de branding son XML válido.
- Tailwind recompilado después de los cambios visuales.

## Consideraciones de producción

La configuración de producción incluye redirección HTTPS, cookies seguras y HSTS configurables.

Antes de desplegar se debe:

- definir una `SECRET_KEY` larga y aleatoria;
- confirmar si todos los subdominios utilizarán HTTPS antes de activar `SECURE_HSTS_INCLUDE_SUBDOMAINS`;
- confirmar la política de preload antes de activar `SECURE_HSTS_PRELOAD`;
- configurar la entrega de static y media en la infraestructura de producción.

## Cierre y estado de reanudación

El sistema se considera funcionalmente concluido como versión candidata estable
`1.0.0`. El estado vigente corresponde al último commit disponible en `main` y
está validado mediante 131 pruebas, sin migraciones pendientes y con revisión
visual completada.

No existe desarrollo obligatorio pendiente. Paginación, filtros, pruebas
reales de navegador, integraciones y nuevas líneas de negocio son mejoras
evolutivas opcionales. La configuración de dominio, respaldos automáticos
externos, HTTPS y endurecimiento del entorno corresponde al proceso de
despliegue administrado por el usuario.

Para una futura modificación se debe leer primero `docs/proximo_paso.md`, donde
se conserva el texto de reanudación y las reglas permanentes del proyecto.
