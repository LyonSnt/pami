# Componentes

## Objetivo

Documentar todos los componentes reutilizables del proyecto.

Los componentes representan únicamente la interfaz.

Nunca contienen lógica de negocio.

---

# Organización

templates/

components/

---

## UI

button.html

Botón principal reutilizable.

Variantes oficiales:

- `primary`: acción principal, utilizada por defecto;
- `secondary`: acción secundaria con borde institucional;
- `inverse`: acción sobre fondos oscuros.

Parámetros:

- `href`;
- `label`;
- `variant`, opcional;
- `element="button"`, opcional, para renderizar un botón de acción;
- `type`, opcional cuando `element="button"`.

---

empty_state.html

Estado vacío.

Se utiliza cuando una colección no tiene registros.

---

card_media.html

Media reutilizable de las cards. Renderiza la imagen del contenido y utiliza el icono oficial como fallback decorativo.

Parámetros:

- `image`;
- `alt`.

---

breadcrumb.html

Navegación jerárquica.

Recibe la estructura desde la vista.

---

## Layout

section_title.html

Título estándar de una sección.

---

## Sections

hero.html

Cabecera principal.

Muestra como etiqueta contextual `SiteConfiguration.hero_label`. Cuando ese campo está vacío, utiliza como respaldo el nombre de la línea seleccionada en `SiteConfiguration.featured_business`. Esta separación permite mostrar `Creaciones Hadasha` como nombre comercial en el catálogo y conservar la composición visual `CREACIONES / HADASHA` en el Home. El eslogan global pertenece al bloque de marca del header y no se utiliza como etiqueta promocional del Hero.

---

benefits.html

Bloque reutilizable de beneficios mostrado actualmente dentro del Hero.

Presenta mensajes generales de Pámi, independientes de la línea destacada:

- **Cuidamos los detalles:** En cada producto y servicio.
- **Entrega confiable:** Acordamos tiempos contigo.
- **Atención cercana:** Te ayudamos a elegir.

Los textos están definidos en la plantilla y no son administrables desde el
CMS. Se mantienen breves para facilitar la lectura en las tres columnas y
evitar promesas absolutas de calidad o rapidez. Utiliza un check para el cuidado
de los detalles, un camión con trazos que no atraviesan las ruedas para la
entrega y una burbuja de conversación para la atención cercana. Los iconos SVG
son decorativos, con tamaño `h-5 w-5`, trazo de grosor 2 y color institucional
sobre fondo suave. El bloque muestra una columna en móvil y tres desde el
breakpoint `sm`.

---

call_to_action.html

Llamado a la acción.

---

## Cards

business_card.html

Tarjeta de línea de negocio.

---

product_card.html

Tarjeta de producto.

---

project_card.html

Tarjeta de proyecto.

---

post_card.html

Tarjeta de artículo.

---

# Convenciones

Los componentes:

- no realizan consultas a base de datos;
- no contienen lógica de negocio;
- reciben datos desde la vista;
- pueden reutilizarse en cualquier página.

---

# Nomenclatura

Se utilizan nombres descriptivos.

Correcto:

button.html

call_to_action.html

business_card.html

Incorrecto:

btn.html

cta.html

card1.html

---

# Filosofía Lyon Dev

Una página se construye mediante componentes.

Los componentes forman un sistema.

No se copia HTML entre páginas.

## Componentes existentes

### UI

- button.html
- empty_state.html
- breadcrumb.html
- card_media.html

### Layout

- section_title.html

### Sections

- hero.html
- benefits.html
- call_to_action.html

### Cards

- business_card.html
- product_card.html
- project_card.html
- post_card.html

## Regla

Los componentes no deben contener lógica de negocio.

Deben recibir datos desde vistas, selectors o context processors.

Las variantes visuales se resuelven dentro del componente oficial. No se debe duplicar el HTML de un botón en otros componentes.
