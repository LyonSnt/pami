# Accesibilidad

## Objetivo

El portal debe poder utilizarse con teclado, lectores de pantalla y diferentes niveles de visión.

## Estructura

- Mantener una jerarquía de encabezados coherente.
- Utilizar elementos semánticos como `header`, `nav`, `main`, `section`, `article` y `footer`.
- Proporcionar un enlace para saltar al contenido principal.

## Teclado y foco

- Toda acción debe ser accesible con teclado.
- El foco debe ser visible mediante `focus-visible`.
- No eliminar el outline sin proporcionar un indicador equivalente.

## Enlaces y botones

- Los enlaces navegan y los botones ejecutan acciones.
- Los nombres accesibles deben describir la acción.
- Los enlaces abiertos en otra pestaña utilizan `rel="noopener noreferrer"`.

## Imágenes e iconos

- Toda imagen informativa requiere `alt` descriptivo.
- Las imágenes decorativas utilizan `alt=""`.
- Los iconos decorativos utilizan `aria-hidden="true"`.

## Mensajes y estados

- Los mensajes importantes utilizan roles apropiados.
- La página actual se indica con `aria-current="page"` cuando corresponda.
- Los errores de formulario se asocian con su control.

## Contraste

Los colores de texto y controles deben conservar contraste suficiente. El color nunca es el único medio para comunicar un estado.
