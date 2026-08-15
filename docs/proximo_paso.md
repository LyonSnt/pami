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

## Despliegue temporal completado

Pámi está desplegado y accesible mediante la IP del VPS y el puerto `8025` sobre HTTP temporal.

Estado confirmado:

- Nginx publica `8025` y reenvía a Gunicorn en `127.0.0.1:8026`;
- el sistema Agua conserva el puerto `80` y su backend en `127.0.0.1:8015`;
- PostgreSQL no tiene exposición pública;
- migraciones, static, media y contenido `seed_demo` funcionan;
- Home, navegación e imágenes cargan correctamente;
- `check --deploy` presenta solo las cuatro advertencias esperadas por operar sin HTTPS: HSTS, redirección SSL y cookies seguras.

La IP y cualquier credencial deben mantenerse fuera del repositorio.

El repositorio ya incluye:

- `docker-compose.prod.yml` sin exposición pública de PostgreSQL y con Gunicorn limitado a `127.0.0.1:8026`;
- imagen multietapa con dependencias de producción y compilación de Tailwind;
- arranque con migraciones, `collectstatic` y Gunicorn;
- plantilla Nginx para static, media y proxy HTTP temporal en el puerto `8025`;
- `.env.production.example` sin secretos;
- procedimiento completo en `docs/despliegue.md`.

## Próximo paso para reanudar

1. Rotar la `SECRET_KEY` y la contraseña PostgreSQL de Agua que fueron expuestas durante la revisión.
2. Revisar los firewalls del sistema y de Hetzner; decidir si `8025` quedará público o limitado a una IP de administración.
3. Completar una prueba funcional de catálogo, portafolio, blog, buscador y contacto con datos no sensibles.
4. Crear y comprobar copias de seguridad de PostgreSQL, media y `.env` antes de administrar contenido real.
5. Configurar dominio, DNS y HTTPS; luego activar redirección SSL y cookies seguras.
6. Mantener HSTS en `0` hasta verificar por completo el portal mediante HTTPS.

## Después

Continuar con el roadmap oficial:

1. Dominio, HTTPS y cierre de la preparación productiva.
2. Filtros de catálogo, portafolio y blog.
3. Optimización de rendimiento y assets.

## Regla de reanudación

No activar `SECURE_SSL_REDIRECT`, cookies seguras ni HSTS mientras el acceso continúe exclusivamente por IP y HTTP. No usar datos personales o credenciales reutilizadas antes de disponer de HTTPS.
