# Layout

## Objetivo

Definir la estructura visual común del portal público.

## Contenedor principal

Las secciones generales utilizan:

```html
max-w-7xl mx-auto px-4 sm:px-6 lg:px-8
```

Se permiten contenedores más estrechos en páginas de lectura, formularios y detalles cuando exista una necesidad de legibilidad:

- `max-w-3xl`: formularios y confirmaciones;
- `max-w-4xl`: lectura editorial;
- `max-w-5xl`: detalles con contenido amplio.

Todos conservan `mx-auto px-4 sm:px-6 lg:px-8`.

## Secciones

Las secciones principales utilizan `py-16`.

Los fondos alternan únicamente entre los colores aprobados, principalmente `bg-white` y `bg-slate-50`.

## Grids

Los listados utilizan una base de una columna y progresan según el contenido:

```html
grid gap-6 sm:grid-cols-2 lg:grid-cols-3
```

## Regla

No crear un layout nuevo si el contenido puede resolverse con el contenedor, sección o grid oficial.
