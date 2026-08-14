# Colores

## Objetivo

Definir la paleta oficial del proyecto.

---

# Color primario

HEX

#E31B23

Uso en Tailwind CSS v4

El proyecto debe registrar este valor como color institucional para evitar sustituirlo por colores aproximados de la paleta predeterminada.

Tokens oficiales:

```text
primary
primary-hover
```

Ejemplos:

```html
bg-primary
text-primary
border-primary
hover:bg-primary-hover
focus-visible:ring-primary
```

Uso

- Botones principales
- Enlaces principales
- Acciones importantes

Hover

#C8161D

---

# Color secundario

White

#FFFFFF

Uso

- Fondo de tarjetas
- Formularios
- Navbar

---

# Fondo general

slate-50

#F8FAFC

Uso

- Fondo principal del sitio

---

# Texto

Título

slate-900

Texto normal

slate-700

Texto secundario

slate-500

---

# Estados

Success

green-600

Warning

amber-500

Danger

#E31B23

Info

blue-600

---

# Regla

No utilizar colores arbitrarios.

Siempre utilizar la paleta oficial.

No utilizar `red-600` como sustituto del rojo institucional, porque su valor `#DC2626` no coincide con el color oficial de Pámi.

Se permiten transparencias del token institucional, por ejemplo `bg-primary/10`, cuando se necesite un fondo de énfasis suave.
