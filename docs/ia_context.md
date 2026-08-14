# IA Context - Pámi (Lyon Dev)

# IMPORTANTE

Antes de realizar cualquier cambio en el proyecto, la IA debe leer obligatoriamente, en este orden:

1. `docs/ia_context.md`
2. `docs/proximo_paso.md`
3. `docs/arquitectura.md`
4. `docs/convenciones.md`
5. `docs/common.md`
6. `docs/design-system/`
7. `docs/estado_actual.md`

No asumir decisiones arquitectónicas sin revisar estos documentos.

---

# Objetivo del proyecto

Pámi es un portal web/CMS desarrollado con Django.

No es un ERP.

No es un e-commerce.

No es un CRM.

Su objetivo es administrar una marca principal con múltiples líneas de negocio desde un único portal.

El proyecto sigue el estándar Lyon Dev.

---

# Filosofía Lyon Dev

Principios:

- Arquitectura limpia.
- Diseño antes de implementar.
- Documentación primero.
- Componentes reutilizables.
- Separación de responsabilidades.
- Evolución progresiva.
- No introducir complejidad anticipada.
- Mantener consistencia visual mediante el Design System.

Nunca improvisar arquitectura.

Nunca implementar primero si el diseño aún no está definido.

---

# Stack oficial

- Python 3.12-slim
- Django
- PostgreSQL 17-alpine
- Docker Compose
- Pillow
- Tailwind CSS v4
- HTMX (planificado)

---

# Docker

Todo el desarrollo se realiza con Docker.

Nunca usar SQLite.

Nunca desarrollar fuera de Docker.

Todos los comandos deben ejecutarse mediante Docker Compose.

---

# PostgreSQL

Versión oficial:

`17-alpine`

Configurada mediante `.env`.

La versión se obtiene desde:

`POSTGRES_VERSION`

---

# Arquitectura

La configuración está modularizada en:

```text
config/settings/components/
```

Las URLs públicas se registran en:

```text
config/urls/public.py
```

---

# Apps

Todas las apps viven dentro de:

```text
apps/
```

Nunca en la raíz.

Las apps no se crean con `startapp`.

Las apps se crean copiando:

```text
tools/generators/app
```

Después de copiar una app:

- ajustar `apps.py`;
- registrar la clase `Config` en `LOCAL_APPS`.

---

# Templates

Las plantillas públicas viven en:

```text
templates/
```

No colocar templates dentro de las apps salvo necesidad técnica.

Template base:

```text
templates/base/base.html
```

Los parciales del layout viven en:

```text
templates/base/
```

Los componentes reutilizables viven en:

```text
templates/components/
```

Organizados por responsabilidad.

---

# Componentes

El proyecto utiliza componentes reutilizables.

Ejemplos:

UI

- button
- empty_state
- breadcrumb
- card_media

Cards

- business_card
- product_card
- project_card
- post_card

Sections

- hero
- benefits
- call_to_action

Layout

- section_title

No duplicar HTML.

Siempre reutilizar componentes existentes.

---

# Design System

Existe un Design System documentado en:

```text
docs/design-system/
```

Debe respetarse antes de modificar cualquier interfaz.

Actualmente incluye:

- Branding
- Colores
- Tipografía
- Espaciados
- Componentes
- Layout
- Formularios
- Iconos
- Responsive
- Accesibilidad

---

# Branding

La identidad visual oficial del proyecto utiliza:

Marca

Pámi

Eslogan

Donde encuentras todo para ti.

Propuesta de valor

Chaquetas y buzos hechos para ti.

Tipografía

Inter

Colores

Primario

#E31B23

Hover

#C8161D

Texto principal

#0D1117

Fondo

#F6F7F9

Los recursos gráficos oficiales viven en:

```text
static/assets/branding/
```

---

# Estado actual

## Infraestructura

- Docker
- PostgreSQL
- Docker Compose
- Dockerfile
- Tailwind CSS v4
- Healthcheck de PostgreSQL
- Servicio Tailwind aislado en Docker

## Backend

Implementadas:

- Common
- Audit
- Accounts
- Site
- Businesses
- Catalog
- Portfolio
- Blog
- Contact

## Frontend

Implementado y pendiente de validación visual final con contenido real.

Incluye:

- Navbar dinámica
- Hero administrable
- Home modular
- Componentes reutilizables
- Empty State
- Breadcrumb
- Cards reutilizables
- CTA
- Footer inicial
- Navegación móvil accesible
- Skip link y foco visible
- Formulario de contacto accesible
- Tokens oficiales de marca
- Recursos SVG oficiales
- Media reutilizable en cards

El Home basado en componentes se encuentra implementado y debe validarse visualmente contra el mockup aprobado utilizando imágenes y contenido representativos.

El enfoque editorial actual del Home es `Confecciones` para público general. Presenta únicamente los productos administrables `Chaquetas` y `Buzos`, junto con proyectos publicados de esa misma línea. Papelería y Tecnología continúan siendo compatibles con la arquitectura, pero no son protagonistas del Home en esta etapa.

La línea protagonista se selecciona mediante `SiteConfiguration.featured_business`. No se debe fijar un slug de negocio en el Home. El eslogan global se muestra junto al logo y el Hero utiliza el nombre de la línea destacada como etiqueta contextual.

`Chaquetas` y `Buzos` son registros de `Product`, no categorías ni líneas de negocio. No existe todavía un modelo `ProductCategory` porque el catálogo actual no requiere esa complejidad.

El bloque de beneficios del Hero fue extraído a:

```text
templates/components/sections/benefits.html
```

El Hero reutiliza este componente y no duplica su HTML.

## Calidad

- Los selectors públicos aplican reglas completas de visibilidad.
- Las operaciones administrativas principales generan auditoría.
- La suite actual contiene 33 pruebas.
- `manage.py check` no reporta problemas.
- No existen cambios de migración pendientes al cierre de la última validación.
- El demo de desarrollo publica Confecciones con Chaquetas y Buzos; los registros demo anteriores conocidos permanecen conservados pero despublicados.

---

# Orden oficial de desarrollo

1. Infraestructura
2. Backend
3. Capa pública
4. Design System
5. UI/UX
6. SEO
7. Buscador
8. Filtros
9. Optimización

---

# Reglas

Nunca colocar lógica de negocio en Views.

Toda lógica de negocio pertenece a Services.

Consultas reutilizables pertenecen a Selectors.

No duplicar componentes.

No duplicar HTML.

Mantener el Design System.

Mantener la arquitectura existente.

Antes de proponer cambios:

- analizar;
- revisar documentación;
- proponer mejoras si aportan valor.

No modificar decisiones ya aprobadas sin justificar el motivo.

---

# Protocolo de trabajo

Cada tarea debe seguir este flujo:

1. Analizar.
2. Revisar documentación.
3. Diseñar.
4. Proponer mejoras arquitectónicas si existen.
5. Esperar aprobación.
6. Implementar.
7. Probar.
8. Actualizar la documentación afectada.
9. Actualizar `docs/estado_actual.md`.
10. Actualizar `docs/proximo_paso.md` si cambia el punto de reanudación.

Nunca saltarse estos pasos.
