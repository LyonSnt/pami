# Próximo paso de desarrollo

## Estado actual

Se completaron los nueve bloques derivados de la auditoría integral:

1. Integridad funcional del backend.
2. Pruebas de regresión.
3. Configuración e infraestructura.
4. Services, auditoría y responsabilidades.
5. Fundamentos del Design System.
6. Responsive y accesibilidad global.
7. Consistencia visual y reutilización.
8. Home y branding.
9. Sincronización documental.

Validación vigente:

- 44 pruebas correctas;
- Django check sin problemas;
- sin cambios de migración pendientes;
- Tailwind CSS v4 compilado;
- branding SVG completo.

## Validación visual completada

El portal público fue validado en móvil, tablet y escritorio con imágenes WebP y contenido representativo de Confecciones.

La validación incluyó Home, catálogo, detalles de producto, portafolio, detalles de proyecto, blog, detalles de artículo, formulario de contacto y confirmación de envío.

Se ajustaron proporciones responsive, cuadrículas, páginas de detalle, contenido editorial, formulario y footer. El eslogan, la etiqueta Confecciones, las acciones, las tarjetas y los estados accesibles conservan la jerarquía y las reglas del Design System.

Validación final:

- 44 pruebas correctas;
- Django check sin problemas;
- sin cambios de migración pendientes;
- Tailwind CSS recompilado;
- contenido demo e imágenes cargados de forma idempotente.

## SEO completado

La fase de SEO técnico y contenido SEO esencial quedó implementada:

1. Títulos y metadescripciones específicos en las páginas públicas.
2. Canonical, Open Graph y Twitter Cards.
3. `robots.txt` y sitemap con contenido público vigente.
4. Confirmación de contacto con `noindex, follow`.
5. Un único `h1` en los listados principales y jerarquía preservada en el Home.
6. Breadcrumbs completos en detalles de Blog y Portafolio.
7. Pruebas de metadatos, robots y exclusión de contenido no publicado.

## Buscador implementado

El portal dispone de una búsqueda real mediante `/buscar/`:

- consulta productos, proyectos, artículos y líneas de negocio;
- conserva las reglas existentes de actividad, publicación y fecha;
- agrupa los resultados por tipo reutilizando las tarjetas oficiales;
- incluye estados inicial y sin resultados;
- ofrece acceso desde el encabezado de escritorio y el menú móvil;
- utiliza canonical estable y `noindex, follow`;
- limita cada grupo a seis coincidencias en esta primera versión.

## Validación del buscador completada

La presentación inicial del buscador fue aprobada. El campo y su acción utilizan una variante grande, los estados informativos conservan el mismo ancho de lectura y el acceso mediante lupa se integra con el encabezado.

## Próximo paso

Validar el primer despliegue en un VPS Hetzner CX23 mediante la dirección IP y HTTP temporal. La dirección IP del servidor y cualquier credencial deben mantenerse fuera del repositorio.

El repositorio ya incluye:

- `docker-compose.prod.yml` sin exposición pública de PostgreSQL y con Gunicorn limitado a `127.0.0.1:8026`;
- imagen multietapa con dependencias de producción y compilación de Tailwind;
- arranque con migraciones, `collectstatic` y Gunicorn;
- plantilla Nginx para static, media y proxy HTTP temporal en el puerto `8025`;
- `.env.production.example` sin secretos;
- procedimiento completo en `docs/despliegue.md`.

El despliegue debe definir y validar:

1. variables de entorno y `SECRET_KEY` de producción;
2. dominio, DNS y `ALLOWED_HOSTS`;
3. proxy inverso y certificados TLS;
4. entrega persistente de static y media;
5. persistencia y copias de seguridad de PostgreSQL;
6. ejecución de migraciones y recolección de static;
7. firewall con exposición exclusiva de los servicios necesarios;
8. `check --deploy`, prueba funcional y verificación de restauración.

## Después

Continuar con el roadmap oficial:

1. Preparación y ejecución del primer despliegue.
2. Filtros de catálogo, portafolio y blog.
3. Optimización de rendimiento y assets.

## Preparación de producción pendiente

Antes del despliegue:

- configurar una `SECRET_KEY` segura;
- decidir HSTS para subdominios y preload;
- definir el servicio de static y media;
- ejecutar `check --deploy` con las variables reales de producción.

## Regla de reanudación

No exponer el portal a Internet hasta completar la configuración de producción, TLS, firewall, persistencia y copias de seguridad.
