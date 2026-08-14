# Responsive

## Enfoque

El portal sigue un enfoque mobile-first.

Los estilos sin prefijo corresponden a móvil. Los prefijos `sm:`, `md:` y `lg:` se añaden cuando el contenido requiere progresión real.

## Contenedores

```html
px-4 sm:px-6 lg:px-8
```

## Grids

Los listados parten de una columna:

```html
grid gap-6 sm:grid-cols-2 lg:grid-cols-3
```

## Tipografía

Los títulos principales escalan de forma progresiva. No se debe imponer el tamaño de escritorio en móvil.

## Navegación

La navegación principal debe permanecer disponible en todos los tamaños. Ocultar el menú de escritorio exige proporcionar una alternativa móvil accesible.

## Acciones

Los grupos de botones deben permitir `flex-wrap` o apilarse en pantallas estrechas.

## Verificación mínima

Cada interfaz se revisa al menos en anchos representativos de móvil, tablet y escritorio.
