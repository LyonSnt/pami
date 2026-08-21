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

- 101 pruebas correctas;
- Django check sin problemas;
- sin cambios de migración pendientes;
- Tailwind CSS v4 compilado;
- branding SVG completo.

## Validación visual completada

El portal público fue validado en móvil, tablet y escritorio con imágenes WebP y contenido representativo de Confecciones.

La validación incluyó Home, catálogo, detalles de producto, portafolio, detalles de proyecto, blog, detalles de artículo, formulario de contacto y confirmación de envío.

Se ajustaron proporciones responsive, cuadrículas, páginas de detalle, contenido editorial, formulario y footer. El eslogan, la etiqueta Confecciones, las acciones, las tarjetas y los estados accesibles conservan la jerarquía y las reglas del Design System.

Validación final:

- 101 pruebas correctas;
- Django check sin problemas;
- sin cambios de migración pendientes;
- Tailwind CSS recompilado;
- contenido demo e imágenes cargados de forma idempotente.

## SEO completado

La fase de SEO técnico y contenido SEO esencial quedó implementada:

1. Títulos y metadescripciones específicos en las páginas públicas.
2. Canonical, Open Graph y Twitter Cards.
3. `robots.txt` y sitemap con contenido público vigente.
4. Confirmación de contacto con `noindex, follow`.
5. Un único `h1` en los listados principales y jerarquía preservada en el Home.
6. Breadcrumbs completos en detalles de Blog y Portafolio.
7. Pruebas de metadatos, robots y exclusión de contenido no publicado.

La ampliación de SEO social y datos estructurados incorpora:

1. `twitter:image` y tarjeta grande cuando existe una imagen específica o de respaldo.
2. Resolución centralizada de URLs absolutas para imágenes sociales.
3. `Organization` global con identidad, contacto y redes configuradas.
4. `Product` con línea, marca y oferta únicamente cuando el precio es visible.
5. `BlogPosting` con fechas, descripción, imagen y organización editora.
6. Serialización JSON-LD que neutraliza caracteres capaces de cerrar el elemento `script`.

No se declaran inventario, reseñas, valoraciones ni información que el CMS no administra. Los proyectos permanecen sin un esquema específico hasta disponer de datos suficientes para representarlos correctamente.

## Buscador implementado

El portal dispone de una búsqueda real mediante `/buscar/`:

- consulta productos, proyectos, artículos y líneas de negocio;
- conserva las reglas existentes de actividad, publicación y fecha;
- agrupa los resultados por tipo reutilizando las tarjetas oficiales;
- incluye estados inicial y sin resultados;
- ofrece acceso desde el encabezado de escritorio y el menú móvil;
- utiliza canonical estable y `noindex, follow`;
- limita cada grupo a seis coincidencias en esta primera versión.

## Validación del buscador completada

La presentación inicial del buscador fue aprobada. El campo y su acción utilizan una variante grande, los estados informativos conservan el mismo ancho de lectura y el acceso mediante lupa se integra con el encabezado.

## Despliegue temporal completado

Pámi está desplegado y accesible mediante la IP del VPS y el puerto `8025` sobre HTTP temporal.

Estado confirmado:

- Nginx publica `8025` y reenvía a Gunicorn en `127.0.0.1:8026`;
- el sistema Agua conserva el puerto `80` y su backend en `127.0.0.1:8015`;
- PostgreSQL no tiene exposición pública;
- migraciones, static, media y contenido `seed_demo` funcionan;
- Home, navegación e imágenes cargan correctamente;
- `check --deploy` presenta solo las cuatro advertencias esperadas por operar sin HTTPS: HSTS, redirección SSL y cookies seguras.

La IP y cualquier credencial deben mantenerse fuera del repositorio.

El repositorio ya incluye:

- `docker-compose.prod.yml` sin exposición pública de PostgreSQL y con Gunicorn limitado a `127.0.0.1:8026`;
- imagen multietapa con dependencias de producción y compilación de Tailwind;
- arranque con migraciones, `collectstatic` y Gunicorn;
- plantilla Nginx para static, media y proxy HTTP temporal en el puerto `8025`;
- `.env.production.example` sin secretos;
- procedimiento completo en `docs/despliegue.md`.

## Próximo paso para reanudar

1. Rotar la `SECRET_KEY` y la contraseña PostgreSQL de Agua que fueron expuestas durante la revisión.
2. Revisar los firewalls del sistema y de Hetzner; decidir si `8025` quedará público o limitado a una IP de administración.
3. Completar una prueba funcional de catálogo, portafolio, blog, buscador y contacto con datos no sensibles.
4. Crear y comprobar copias de seguridad de PostgreSQL, media y `.env` antes de administrar contenido real.
5. Configurar dominio, DNS y HTTPS; luego activar redirección SSL y cookies seguras.
6. Mantener HSTS en `0` hasta verificar por completo el portal mediante HTTPS.

## Después

Continuar con el roadmap oficial:

1. Dominio, HTTPS y cierre de la preparación productiva.
2. Filtros de catálogo, portafolio y blog.
3. Generación de variantes responsive para nuevas imágenes editoriales, cuando el volumen de contenido lo justifique.

## Rendimiento y assets

La primera optimización de rendimiento quedó completada:

- el Home reutiliza la configuración global dentro de la misma petición;
- existen pruebas de regresión para los presupuestos de consultas del Home y el buscador;
- la plantilla de Nginx comprime respuestas de texto y SVG;
- los archivos estáticos usan nombres versionados por contenido y se almacenan en el navegador durante 30 días;
- las imágenes demo continúan en WebP y su conjunto permanece por debajo de 450 KB.

Los filtros y la paginación se posponen hasta que el volumen real supere la presentación actual. La generación automática de imágenes responsive también queda diferida para evitar complejidad sin beneficio visible en esta etapa.

## Administración editorial

La revisión funcional del panel administrativo quedó completada:

- los editores pueden gestionar de forma explícita los estados `Activo` y `Publicado`;
- la configuración única del sitio no puede eliminarse desde el administrador;
- las imágenes admiten JPG, PNG y WebP hasta 5 MB;
- los enlaces editoriales aceptan rutas internas, anclas y URLs HTTP/HTTPS;
- las reglas están cubiertas por pruebas y migraciones declarativas sin transformación de datos.

## Seguridad del administrador

El comando idempotente `setup_admin_roles` mantiene dos grupos oficiales:

- `Editor de contenido`: puede consultar, crear y modificar configuración, navegación, líneas, productos, proyectos y publicaciones;
- `Gestor de contacto`: puede consultar mensajes y ejecutar sus transiciones de estado.

Ninguno puede eliminar contenido, administrar usuarios ni consultar registros de auditoría. Estas operaciones permanecen reservadas al superusuario. Los mensajes tampoco pueden crearse, eliminarse o reasignarse manualmente desde el administrador. Los inicios y cierres de sesión quedan auditados.

Las entradas administrativas de cuentas se distinguen como `Usuarios` y `Perfiles de usuario`. La primera administra autenticación, grupos y permisos; la segunda conserva teléfono y zona horaria sin duplicar cuentas ni datos.

## Integridad editorial

La configuración `Modo mantenimiento` ya es funcional:

- el portal responde con HTTP 503 y una página responsive excluida de indexación;
- Django Admin, static y media permanecen accesibles;
- los usuarios staff autenticados pueden revisar el portal antes de reabrirlo.

Los productos solo pueden mostrar un precio cuando existe un valor positivo. La regla se aplica tanto en formularios y modelos como mediante restricciones de PostgreSQL. La publicación programada del Blog y la exclusión de contenido perteneciente a líneas inactivas ya eran correctas y se conservaron sin cambios.

## Manejo de errores públicos

Las respuestas 404 y 500 utilizan páginas responsive con identidad Pámi, acciones para recuperar la navegación y `noindex, nofollow`. Conservan sus códigos HTTP correctos. La respuesta 500 no usa configuración, navegación ni consultas a base de datos, por lo que puede mostrarse incluso durante un fallo de infraestructura o persistencia.

## Protección del contacto

El formulario de contacto incluye un honeypot invisible y descarta silenciosamente envíos automatizados. También evita guardar dos veces el mismo contenido dentro de una ventana configurable de 60 segundos por sesión, sin impedir un nuevo contacto posterior.

Los accesos desde una línea, producto o proyecto preseleccionan únicamente una línea pública y preparan un asunto descriptivo. Adicionalmente, la caché limita por defecto a cinco mensajes aceptados por dirección dentro de diez minutos. La dirección se transforma en un hash para construir la clave temporal y no se almacena en los mensajes ni en la auditoría. Los límites se configuran mediante `CONTACT_RATE_LIMIT_MAX_SUBMISSIONS` y `CONTACT_RATE_LIMIT_WINDOW_SECONDS`.

La notificación por correo se activa únicamente cuando existe `CONTACT_NOTIFICATION_EMAIL`. El mensaje se almacena y audita antes de intentar la entrega; un fallo SMTP se registra, pero no pierde el contacto ni muestra un error al visitante.

## Limpieza de arquitectura

Se retiraron los módulos vacíos heredados del scaffolding inicial y los imports de signals sin implementación. Se conservaron todos los `__init__.py`, paquetes de migraciones, signals funcionales y APIs internas con código. La estructura documentada refleja ahora los templates y componentes reales del portal.

## Ajuste del logotipo móvil

El nombre `Pámi` del logotipo SVG utiliza un único flujo de texto con segmentos contiguos para sus dos colores. Esto evita separaciones variables entre `Pá` y `mi` según la métrica tipográfica del navegador, sin modificar las dimensiones ni los colores oficiales.

## Identidad y contacto administrables

El portal utiliza el logo y favicon cargados en `SiteConfiguration` cuando existen y conserva los SVG oficiales como respaldo. El footer convierte el correo, teléfono y WhatsApp configurados en acciones directas y muestra únicamente las redes sociales que tengan una URL definida. Los enlaces externos se abren de forma segura y la navegación de redes dispone de una etiqueta accesible.

## Navegación activa y menú móvil

La navegación identifica la ruta actual sin depender de la etiqueta editorial. Los apartados permanecen activos dentro de sus páginas de detalle, Inicio solo se activa en la raíz y los enlaces externos no se marcan por coincidencias accidentales. El estado se presenta visualmente y mediante `aria-current="page"` en escritorio y móvil, incluidos Buscar y Contacto.

El menú móvil conserva `<details>` como base semántica, alterna entre los iconos de menú y cierre, sincroniza `aria-expanded` y se cierra al seleccionar un enlace, pulsar fuera o presionar Escape. Al cerrarse con el teclado, el foco regresa al control de apertura.

## Página de línea de negocio

El detalle de una línea presenta un encabezado responsive con breadcrumb, información editorial, imagen administrable y acciones hacia catálogo y contacto contextual. Resume hasta dos productos, dos proyectos y dos artículos públicos mediante las cards oficiales y ofrece accesos a sus listados completos.

Las secciones sin contenido se omiten; cuando la línea no tiene ninguna publicación relacionada se presenta un único estado vacío. Los selectores conservan las reglas de actividad, publicación y fecha, y el detalle dispone de un presupuesto de seis consultas. `seed_demo` completa la imagen representativa de Confecciones únicamente cuando el campo está vacío.

## Regla de reanudación

No activar `SECURE_SSL_REDIRECT`, cookies seguras ni HSTS mientras el acceso continúe exclusivamente por IP y HTTP. No usar datos personales o credenciales reutilizadas antes de disponer de HTTPS.
