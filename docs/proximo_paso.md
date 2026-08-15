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

- 33 pruebas correctas;
- Django check sin problemas;
- sin cambios de migración pendientes;
- Tailwind CSS v4 compilado;
- branding SVG completo.

## Validación visual completada

El portal público fue validado en móvil, tablet y escritorio con imágenes WebP y contenido representativo de Confecciones.

La validación incluyó Home, catálogo, detalles de producto, portafolio, detalles de proyecto, blog, detalles de artículo, formulario de contacto y confirmación de envío.

Se ajustaron proporciones responsive, cuadrículas, páginas de detalle, contenido editorial, formulario y footer. El eslogan, la etiqueta Confecciones, las acciones, las tarjetas y los estados accesibles conservan la jerarquía y las reglas del Design System.

Validación final:

- 33 pruebas correctas;
- Django check sin problemas;
- sin cambios de migración pendientes;
- Tailwind CSS recompilado;
- contenido demo e imágenes cargados de forma idempotente.

## Próximo paso

Iniciar la fase de SEO técnico y contenido SEO.

### Alcance

1. Revisar títulos, descripciones y metadatos de todas las páginas públicas.
2. Incorporar canonical, Open Graph y metadatos sociales cuando corresponda.
3. Definir `robots.txt` y sitemap.
4. Revisar estructura de encabezados, enlaces internos y contenido indexable.
5. Validar el resultado con Django check y la suite completa.

Esta fase no debe introducir nuevos componentes si los existentes pueden resolver el ajuste.

## Después

Continuar con el roadmap oficial:

1. SEO técnico y contenido SEO.
2. Buscador real.
3. Filtros de catálogo, portafolio y blog.
4. Optimización de rendimiento y assets.
5. Preparación de despliegue.

## Preparación de producción pendiente

Antes del despliegue:

- configurar una `SECRET_KEY` segura;
- decidir HSTS para subdominios y preload;
- definir el servicio de static y media;
- ejecutar `check --deploy` con las variables reales de producción.

## Regla de reanudación

No comenzar SEO ni buscador hasta completar y aprobar la validación visual final.
