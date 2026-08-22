# Reanudación futura de Pámi

## Sistema concluido

Pámi se considera funcionalmente concluido como versión candidata estable
`1.0.0`. El último commit de cierre funcional es:

```text
fa526c2 mejora:agregar-respaldo-manual-desde-admin
```

No existe un bloque obligatorio de desarrollo pendiente. Cualquier cambio
posterior debe responder a una nueva necesidad de contenido, negocio,
integración o infraestructura.

## Validación vigente

- 114 pruebas correctas;
- `python manage.py check` sin problemas;
- `makemigrations --check --dry-run` sin cambios pendientes;
- portal validado en móvil, tablet y escritorio;
- ampliación accesible en todas las imágenes públicas de contenido;
- variantes responsive WebP para Hero, tarjetas y detalles;
- respaldo manual PostgreSQL exclusivo para superusuarios y auditado;
- documentación de instalación, operación, respaldo y despliegue actualizada.

## Alcance completado

- Home administrable enfocado en Confecciones, Chaquetas y Buzos.
- Líneas de negocio, catálogo, portafolio y Blog.
- Buscador público con reglas de publicación.
- Contacto protegido, contextual, auditable y con notificaciones configurables.
- Navegación responsive con estado activo y comportamiento accesible.
- Roles de edición y contacto, usuarios personalizados y auditoría inmutable.
- SEO técnico, sitemap, `robots.txt`, Open Graph, Twitter Cards y JSON-LD.
- Mantenimiento y páginas públicas 404 y 500.
- Imágenes administrables, ampliables y optimizadas mediante ImageKit.
- Descarga manual de la base PostgreSQL desde Django Admin para superusuarios.

## Mejoras futuras opcionales

Estas mejoras no bloquean la versión actual:

1. Filtros y paginación cuando aumente el volumen real de contenido.
2. Pruebas automatizadas con navegador para recorridos completos.
3. Nuevos tamaños de imagen si cambia la composición editorial.
4. Integraciones externas de correo, analítica o canales comerciales.
5. Nuevas líneas de negocio y sus contenidos.

## Responsabilidades operativas

El despliegue se administra por separado del desarrollo. Antes de utilizar
datos reales se debe completar dominio y HTTPS. También se deben mantener
respaldos automáticos fuera del VPS que incluyan:

- volcado PostgreSQL;
- directorio persistente `media/`;
- copia cifrada del `.env`.

El respaldo descargado desde Django Admin contiene únicamente PostgreSQL y es
un complemento, no un reemplazo de la estrategia automática externa.

## Texto para retomar el proyecto

Copiar el siguiente mensaje en una conversación nueva:

```text
Continuemos con Pámi desde el último commit disponible en main. Lee README.md,
docs/estado_actual.md, docs/proximo_paso.md y la documentación relacionada con
el cambio solicitado. El sistema está funcionalmente concluido como versión
candidata 1.0.0, con 114 pruebas correctas. El despliegue lo manejo yo;
trabajemos exclusivamente en desarrollo. Primero revisa el código y presenta
hallazgos y propuesta, y espera mi aprobación antes de implementar. No uses
PowerShell ni modifiques deploy-data/. El cambio que quiero realizar es:
[DESCRIBIR AQUÍ EL CAMBIO].
```

## Reglas permanentes de trabajo

- No usar PowerShell para ejecutar comandos ni modificar archivos.
- No modificar `deploy-data/`.
- Presentar hallazgos y propuesta antes de cambios visuales o funcionales.
- Esperar aprobación antes de implementar el alcance propuesto.
- Escribir los mensajes de commit en español.
- El usuario realiza `git push` y administra el despliegue.
