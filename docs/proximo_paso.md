# Reanudación futura de Pámi

## Sistema concluido

Pámi se considera funcionalmente concluido como versión candidata estable
`1.0.0`. Para reanudar se debe utilizar el último commit disponible en `main`.

No existe un bloque obligatorio de desarrollo pendiente. Cualquier cambio
posterior debe responder a una nueva necesidad de contenido, negocio,
integración o infraestructura.

## Validación vigente

- 167 pruebas correctas;
- `python manage.py check` sin problemas;
- `makemigrations --check --dry-run` sin cambios pendientes;
- portal validado en móvil, tablet y escritorio;
- ampliación accesible en todas las imágenes públicas de contenido;
- variantes responsive WebP para Hero, tarjetas y detalles;
- respaldo manual PostgreSQL exclusivo para superusuarios y auditado;
- documentación de instalación, operación, respaldo y despliegue actualizada.
- separación implementada entre el nombre comercial `Creaciones Hadasha` y la etiqueta `Creaciones` del Hero.

## Alcance completado

- Home administrable enfocado en Creaciones Hadasha, Chaquetas y Buzos.
- Líneas de negocio, catálogo, portafolio y Blog.
- Buscador público con reglas de publicación.
- Contacto protegido, contextual, auditable y con notificaciones configurables.
- Navegación responsive con estado activo y comportamiento accesible.
- Roles de edición y contacto, usuarios personalizados y auditoría inmutable.
- SEO técnico, sitemap, `robots.txt`, Open Graph, Twitter Cards y JSON-LD.
- Mantenimiento y páginas públicas 404 y 500.
- Imágenes administrables, ampliables y optimizadas mediante ImageKit.
- Descarga manual de la base PostgreSQL desde Django Admin para superusuarios.
- Catálogo preparado para múltiples líneas con galerías, características y estados comerciales.
- Catálogo general organizado como selector de líneas, sin mezclar sus productos o servicios.
- Línea Soluciones digitales y Sistema de gestión de agua bajo cotización.
- Interruptores públicos para Catálogo, Portafolio, Blog y Contacto; únicamente Catálogo activo en la configuración inicial.
- Etiqueta breve del Hero administrable mediante `SiteConfiguration.hero_label`, con respaldo automático en el nombre de la línea destacada.

## Cambio aprobado para cierre

Se encuentra implementada y validada la separación entre la identidad de la
línea y su presentación en el Home:

- el registro `Business` con slug `creaciones` se denomina `Creaciones Hadasha`;
- el catálogo muestra el nombre comercial completo;
- el Hero conserva `CREACIONES` como etiqueta y `HADASHA` como título;
- el nuevo campo `Etiqueta del Hero` se administra desde `Configuración del sitio`;
- si la etiqueta queda vacía, el componente utiliza el nombre de la línea destacada;
- la migración conserva el slug, las URLs, los productos y demás relaciones;
- `seed_demo`, pruebas y documentación fueron actualizados;
- las 131 pruebas, `check` y la comprobación de migraciones finalizaron correctamente.

La revisión visual del Home, el catálogo general y el administrador fue
completada y aprobada por el usuario. El usuario autorizó el commit de estos
cambios; el push y el despliegue permanecen a su cargo.

## Textos por línea aprobados para cierre

Los textos públicos del Home y catálogo se ajustaron al contexto de cada
línea. `Business.featured_title` y `Business.catalog_intro` se administran en
`Líneas de negocio > Textos del catálogo y Home`, con respaldos generales si
se dejan vacíos. Hadasha muestra `Prendas destacadas` y `Conoce nuestras prendas.`.
Las migraciones `businesses.0003` y `0004` están aplicadas en desarrollo; la
segunda completa solo campos vacíos de las líneas conocidas. `seed_demo`
incluye los textos de Hadasha y Soluciones digitales. Las 133 pruebas pasan y
no hay cambios de modelos sin migración. El usuario aprobó el resultado y
autorizó el commit; el push y el despliegue siguen a su cargo.

## Protección del login validada y aprobada para cierre

Se integra `django-axes==8.3.1`, backend y middleware con contadores en
PostgreSQL. Tras 5 fallos se bloquea durante 15 minutos el nombre de usuario;
otros usuarios y el portal público siguen disponibles. Se agregó respuesta
HTTP 429 en español y documentación de desbloqueo en
[Seguridad del administrador](seguridad_admin.md).

Las migraciones `axes` están aplicadas en desarrollo. Se agregaron ocho pruebas
y se adaptó la prueba de auditoría para usar el login HTTP real. El usuario
ejecutó la suite completa y confirmó mediante captura el resultado:
141 pruebas correctas en 19,206 segundos. El usuario autorizó el commit;
el push y el despliegue del bloque siguen a su cargo.

## Ruta administrativa configurable aprobada para cierre

El cambio local de ruta administrativa está implementado y validado:
`ADMIN_URL_PATH` permite un nombre por entorno, con `admin` como valor inicial.
El login y los enlaces internos, el modo mantenimiento y Axes siguen la nueva
ruta. `/admin/` no redirige si se elige otro nombre y responde con el 404
institucional incluso en desarrollo y mantenimiento. `robots.txt` no publica
la ruta administrativa. Las 155 pruebas
de la suite completa pasan y no hay migraciones pendientes. El usuario autorizó
el commit; el push y el despliegue siguen a su cargo. El `.env` real no se modificó;
la elección de ruta se realiza según [Seguridad del administrador](seguridad_admin.md).

## Mensaje de la ruta antigua aprobado para cierre

Cuando `ADMIN_URL_PATH` tiene otro nombre, `/admin`, `/admin/` y sus subrutas
muestran el 404 institucional también en desarrollo y durante mantenimiento,
con el mensaje `Página no disponible` y únicamente `Volver al inicio`,
sin búsqueda, redirección ni indicación de la nueva ruta. La ruta administrativa activa
continúa funcionando y las demás rutas inexistentes conservan su diagnóstico
de desarrollo. Las 22 pruebas de ruta, errores y mantenimiento pasan. El usuario
revisó el resultado y autorizó el commit; el push y el despliegue siguen a su cargo.

## Selección de destacados aprobada para cierre

`Product.is_featured` agrega la casilla `Mostrar en destacados` en
`Catálogo > Productos > Publicación`, visible también como columna y filtro
del listado. El Home muestra hasta dos marcados, activos y publicados de la
línea destacada, por Orden y Nombre, sin modificar el catálogo. No utiliza
productos sin marcar como respaldo. `catalog.0005` y `0006` están aplicadas en
desarrollo; conservan inicialmente los dos productos públicos que se mostraban
por cada línea. Los productos nuevos tienen la casilla desmarcada. `seed_demo`
marca Chaquetas y Buzos. Las 160 pruebas pasan y no hay migraciones pendientes.
El usuario revisó el resultado y autorizó el commit. El despliegue sigue
a cargo del usuario y no requiere ejecutar `seed_demo` en producción.

## Cantidad de destacados configurable aprobada para cierre

Se agregó `SiteConfiguration.featured_products_limit` en
`Configuración del sitio > Destacados del Home`, con rango de 1 a 12 y valor
inicial 2. El Home respeta la cantidad elegida y conserva la selección por
casilla, línea destacada, actividad, publicación y orden. Si hay menos candidatos,
muestra solo los disponibles. La cuadrícula mantiene una columna en móvil
y dos desde `sm`, agregando filas según la cantidad. Se incluyeron validadores
y una restricción de base de datos, y las migraciones `site.0011` y
`catalog.0007`, aplicadas en desarrollo. Las 163 pruebas de la suite completa
pasan y no hay migraciones pendientes. El usuario revisó el resultado y
autorizó el commit; el push y el despliegue siguen a su cargo.

## Corrección de orientación de imágenes aprobada para cierre

Se agregó un procesador de orientación EXIF mediante Pillow antes del recorte
de las variantes WebP. Corrige orientaciones giradas y reflejadas y conserva
las imágenes sin EXIF y los archivos originales. ImageKit cambia la ruta de
caché de las variantes existentes, sin borrados ni necesidad de volver a subir
las fotos. Las pruebas cubren las ocho orientaciones EXIF de JPEG, además de
orientación en PNG y WebP,
fotos sin metadatos y renovación de caché con conservación del original.
Las 167 pruebas pasan y no hay cambios de modelos pendientes. El usuario
revisó el resultado y autorizó el commit; el push y el despliegue siguen a su cargo.

## Mejoras futuras opcionales

Estas mejoras no bloquean la versión actual:

1. Mantener Django 5.2 LTS actualizado dentro de la serie 5.2.
2. Filtros y paginación cuando aumente el volumen real de contenido.
3. Pruebas automatizadas con navegador para recorridos completos.
4. Nuevos tamaños de imagen si cambia la composición editorial.
5. Integraciones externas de correo, analítica o canales comerciales.
6. Nuevas líneas de negocio y sus contenidos.

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
candidata 1.0.0, con 167 pruebas correctas. El despliegue lo manejo yo;
trabajemos exclusivamente en desarrollo. Primero revisa el código y presenta
hallazgos y propuesta, y espera mi aprobación antes de implementar. No uses
PowerShell ni modifiques deploy-data/. Conserva cualquier cambio local pendiente
y revisa su estado antes de actuar. El cambio que quiero realizar es:
[DESCRIBIR AQUÍ EL CAMBIO].
```

## Reglas permanentes de trabajo

- No usar PowerShell para ejecutar comandos ni modificar archivos.
- No modificar `deploy-data/`.
- Presentar hallazgos y propuesta antes de cambios visuales o funcionales.
- Esperar aprobación antes de implementar el alcance propuesto.
- Escribir los mensajes de commit en español.
- El usuario realiza `git push` y administra el despliegue.
