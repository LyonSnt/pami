# Pámi

Portal público y CMS desarrollado con Django para administrar la marca Pámi y sus líneas de negocio. El Home destaca Creaciones Hadasha, con Chaquetas y Buzos, y el catálogo incorpora también Soluciones digitales, bajo el eslogan oficial **“Donde encuentras todo para ti”**. La presentación del Hero conserva la composición **“CREACIONES / HADASHA”** sin reducir el nombre comercial mostrado en el catálogo.

## Funcionalidades

- Home administrable y responsive.
- Nombre comercial de la línea y etiqueta breve del Hero administrables de forma independiente.
- Líneas de negocio, catálogo, portafolio y Blog.
- Catálogo multilínea con estados comerciales, características y galerías.
- Módulos públicos activables desde Django Admin; la configuración inicial deja visible únicamente el catálogo.
- Buscador público con reglas de publicación.
- Formulario de contacto protegido y auditable.
- Roles administrativos para contenido y contacto.
- Respaldo manual de PostgreSQL exclusivo para superusuarios.
- Modo mantenimiento y páginas de error personalizadas.
- SEO técnico, sitemap, Open Graph, Twitter Cards y JSON-LD.
- Navegación accesible y visor de imágenes en todo el contenido público.
- Variantes responsive WebP para tarjetas, detalles y Hero.

## Tecnologías

- Python 3.12 y Django 5.2 LTS.
- PostgreSQL 17.
- Docker Compose.
- Tailwind CSS v4.
- Pillow e ImageKit para procesamiento de imágenes.
- Gunicorn para producción.

## Requisitos

- Docker y Docker Compose.
- Git.

No se requiere instalar Python, PostgreSQL ni Node.js directamente en el equipo.

## Desarrollo local

1. Crear el archivo de entorno a partir de `.env.example`.
2. Sustituir los valores demostrativos de las credenciales locales.
3. Construir e iniciar los servicios:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

4. Cargar el contenido demostrativo en otra terminal:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py seed_demo
```

El portal queda disponible en `http://localhost:8025/` y el administrador en `http://localhost:8025/admin/`, salvo que se modifique `WEB_PORT`.

La ruta del administrador se configura con `ADMIN_URL_PATH` en `.env`;
el valor inicial es `admin`. Por ejemplo, `ADMIN_URL_PATH=panel-pami` utiliza
`/panel-pami/` y deja `/admin/` sin acceso ni redirección. Se requiere recrear
el servicio web para cargar el nuevo valor. Detalles en
[Seguridad del administrador](docs/seguridad_admin.md).

## Comandos de calidad

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py check
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py makemigrations --check --dry-run
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm web python manage.py test
docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm tailwind npm run tailwind
```

La suite estable contiene 163 pruebas.

## Roles administrativos

Para elegir productos del Home, abrir `Catálogo > Productos` y marcar
`Mostrar en destacados` en el bloque `Publicación`. La cantidad se elige en
`Configuración del sitio > Destacados del Home > Cantidad de productos destacados`
(de 1 a 12, inicialmente 2). El Home muestra los marcados de la línea destacada,
activos y publicados, según Orden y Nombre, hasta alcanzar la cantidad elegida.
Desmarcar un producto no lo retira del catálogo. Los productos nuevos quedan
sin marcar.

Los grupos oficiales se crean o actualizan de forma idempotente:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py setup_admin_roles
```

- `Editor de contenido`: gestiona configuración y contenido editorial.
- `Gestor de contacto`: consulta mensajes y administra sus estados.
- El superusuario conserva usuarios, permisos y auditoría.

## Producción

La configuración productiva utiliza `.env.production.example`, `docker-compose.prod.yml` y la imagen multietapa del proyecto. Las instrucciones completas están en [docs/despliegue.md](docs/despliegue.md).

Nunca se deben versionar `.env`, archivos media, copias de base de datos ni `deploy-data/`.

## Documentación

- [Estado actual](docs/estado_actual.md)
- [Próximo paso](docs/proximo_paso.md)
- [Arquitectura](docs/arquitectura.md)
- [Convenciones](docs/convenciones.md)
- [Design System](docs/design-system/README.md)
- [Despliegue](docs/despliegue.md)
- [Seguridad del administrador](docs/seguridad_admin.md)

## Estado

Versión candidata estable `1.0.0`. El despliegue, dominio y TLS dependen de cada entorno.
