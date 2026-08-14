# Sistema de Espaciado

## Objetivo

Definir una escala única de espaciado para todo el proyecto.

Se evita utilizar valores arbitrarios. Todos los componentes y layouts deben seguir esta escala para mantener consistencia visual.

---

# Escala oficial

| Tailwind | Equivalente |
|----------|-------------|
| p-2 | 8 px |
| p-4 | 16 px |
| p-6 | 24 px |
| p-8 | 32 px |
| p-12 | 48 px |
| p-16 | 64 px |
| p-24 | 96 px |

La misma escala aplica para:

- margin (`m-*`)
- padding (`p-*`)
- gap (`gap-*`)
- space (`space-y-*`, `space-x-*`)

---

# Separación entre secciones

Las secciones principales del portal utilizan:

```html
py-16
```

Equivalente:

64 px arriba

64 px abajo

---

# Contenedores

Todos los contenedores públicos utilizan:

```html
max-w-7xl
mx-auto
px-4
sm:px-6
lg:px-8
```

No deben existir contenedores distintos salvo una necesidad justificada.

---

# Espaciado interno de Cards

Las tarjetas utilizan:

```html
p-6
```

---

# Formularios

Separación entre campos:

```html
space-y-5
```

---

# Botones

Padding oficial:

```html
px-5
py-2.5
```

---

# Regla

No utilizar valores arbitrarios.

Ejemplo incorrecto:

```html
mt-[37px]
```

Ejemplo correcto:

```html
mt-10
```

Siempre utilizar la escala oficial de Tailwind.