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

- 30 pruebas correctas;
- Django check sin problemas;
- sin cambios de migración pendientes;
- Tailwind CSS v4 compilado;
- branding SVG completo.

## Próximo paso

Realizar validación visual final contra el mockup aprobado utilizando contenido e imágenes representativas.

### Alcance

1. Cargar o seleccionar imágenes reales para Hero, negocios, productos, proyectos y artículos.
2. Revisar Home en móvil, tablet y escritorio.
3. Revisar páginas internas en los mismos tamaños.
4. Comparar jerarquía, espaciado, proporciones y densidad visual con el mockup.
5. Corregir únicamente diferencias verificadas, reutilizando los componentes y tokens existentes.
6. Ejecutar nuevamente Tailwind, Django check y la suite completa.

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
