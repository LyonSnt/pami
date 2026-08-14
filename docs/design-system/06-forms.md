# Formularios

## Objetivo

Mantener formularios consistentes, legibles y accesibles.

## Estructura

- Cada control debe tener un `label` visible asociado.
- La separación entre campos utiliza `space-y-5`.
- Los formularios contenidos en card utilizan `bg-white`, `border-slate-200`, `p-6` y `rounded-2xl`.
- Los errores se muestran junto al campo y mediante un resumen cuando corresponda.

## Controles

Los inputs, selects y textareas utilizan:

```html
w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-base text-slate-900
```

Estado de foco:

```html
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary
```

## Acciones

Los envíos utilizan el componente o la receta oficial de botón `primary`.

## Regla

No utilizar `form.as_p` en interfaces finales. Los campos se renderizan explícitamente para controlar ayuda, errores y accesibilidad.
