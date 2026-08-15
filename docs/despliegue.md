# Despliegue de Pámi

## Objetivo

Esta guía describe el primer despliegue en un VPS Hetzner mediante Docker Compose, PostgreSQL, Gunicorn y el Nginx instalado en el host.

La primera etapa utiliza la dirección IPv4 del servidor mediante HTTP. Debe considerarse una validación temporal: no se deben ingresar credenciales administrativas ni datos personales reales hasta configurar un dominio y HTTPS.

La IP, contraseñas, llaves privadas y el archivo `.env` nunca deben guardarse en Git.

## Requisitos del servidor

- Ubuntu o Debian actualizado.
- Acceso SSH mediante llave.
- Git, Docker Engine, el complemento Docker Compose y Nginx.
- Firewall con SSH y HTTP habilitados.
- Puerto de PostgreSQL sin exposición pública.

Puertos temporales necesarios:

- `22/tcp` para SSH, restringido por origen cuando sea posible;
- `8025/tcp` para el acceso temporal de Pámi por IP.

El puerto `80/tcp` continúa asignado al sistema existente. El puerto `443/tcp` se habilitará para Pámi al incorporar un dominio y TLS.

## Primera instalación

Clonar el repositorio y entrar en él:

```bash
git clone URL_DEL_REPOSITORIO pami
cd pami
```

Crear el archivo privado de variables:

```bash
cp .env.production.example .env
chmod 600 .env
nano .env
```

Reemplazar obligatoriamente:

- `SECRET_KEY` por una clave larga y aleatoria;
- `DB_PASSWORD` por una contraseña distinta y aleatoria;
- `SERVER_IPV4` en `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` por la IP real.

No utilizar valores demostrativos ni copiar el `.env` de desarrollo.

Crear los directorios persistentes con el UID y GID utilizados por el contenedor:

```bash
sudo install -d -o 10001 -g 10001 -m 755 /opt/pami-data/static
sudo install -d -o 10001 -g 10001 -m 755 /opt/pami-data/media
```

Construir e iniciar la aplicación:

```bash
docker compose --env-file .env -f docker-compose.prod.yml up -d --build
```

El contenedor web ejecuta las migraciones y `collectstatic` antes de iniciar Gunicorn. La recolección excluye `css/input.css`, que es la fuente de Tailwind, y publica su `output.css` compilado y versionado. Gunicorn se publica exclusivamente en `127.0.0.1:8026`; PostgreSQL no se expone al host ni a Internet.

## Configuración temporal de Nginx por IP

Copiar la plantilla incluida y reemplazar `SERVER_IPV4` por la IP real:

```bash
sudo cp deploy/nginx/pami-ip.conf.example /etc/nginx/sites-available/pami
sudo nano /etc/nginx/sites-available/pami
sudo ln -s /etc/nginx/sites-available/pami /etc/nginx/sites-enabled/pami
sudo nginx -t
sudo systemctl reload nginx
```

La configuración publica Pámi en el puerto `8025`, sirve `/static/` y `/media/` desde `/opt/pami-data/`, y reenvía la aplicación a Gunicorn en `127.0.0.1:8026`. También comprime las respuestas de texto y SVG y conserva los archivos estáticos durante 30 días en el navegador. En producción, Django versiona sus nombres según el contenido durante `collectstatic`, por lo que una nueva versión no reutiliza CSS o recursos anteriores.

La URL temporal será:

```text
http://SERVER_IPV4:8025
```

Se debe permitir `8025/tcp` tanto en el firewall de Hetzner como en el firewall del sistema. No se deben abrir `8026/tcp` ni `5432/tcp`.

Revisar el estado y los registros:

```bash
docker compose --env-file .env -f docker-compose.prod.yml ps
docker compose --env-file .env -f docker-compose.prod.yml logs --tail=100 web
sudo nginx -t
```

## Inicialización del portal

Crear el usuario administrador:

```bash
docker compose --env-file .env -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

Crear o sincronizar los roles administrativos oficiales:

```bash
docker compose --env-file .env -f docker-compose.prod.yml exec web python manage.py setup_admin_roles
```

El superusuario asigna desde Django Admin el grupo `Editor de contenido` o `Gestor de contacto` a cada usuario staff. No se deben conceder permisos de usuarios o auditoría fuera de cuentas superusuario.

## Notificaciones de contacto

Las notificaciones permanecen desactivadas mientras `CONTACT_NOTIFICATION_EMAIL` esté vacío. Cuando exista un proveedor SMTP, configurar en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=Pámi <no-reply@dominio.example>
CONTACT_NOTIFICATION_EMAIL=equipo@dominio.example
EMAIL_HOST=smtp.proveedor.example
EMAIL_PORT=587
EMAIL_HOST_USER=usuario-smtp
EMAIL_HOST_PASSWORD=secreto-smtp
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_TIMEOUT=10
```

No se deben versionar las credenciales SMTP. Después de configurarlas, realizar un envío real y confirmar tanto el registro en Django Admin como la recepción del correo. Si SMTP falla, el mensaje permanece almacenado y el error aparece en los registros de la aplicación.

Si se desea cargar el contenido inicial aprobado de Confecciones:

```bash
docker compose --env-file .env -f docker-compose.prod.yml exec web python manage.py seed_demo
```

Verificar Django en modo de despliegue:

```bash
docker compose --env-file .env -f docker-compose.prod.yml exec web python manage.py check --deploy
```

Durante la etapa HTTP aparecerán advertencias relacionadas con HTTPS. Deben resolverse al configurar el dominio; no deben silenciarse modificando el código.

## Actualizaciones

Antes de actualizar, crear una copia de seguridad de la base y del volumen de media. Después:

```bash
git pull --ff-only
docker compose --env-file .env -f docker-compose.prod.yml up -d --build
docker compose --env-file .env -f docker-compose.prod.yml ps
```

Las migraciones y la recolección de static se ejecutan durante el inicio del nuevo contenedor web.

## Copias de seguridad

Crear un directorio privado fuera del repositorio:

```bash
mkdir -p ../pami-backups
chmod 700 ../pami-backups
```

La copia debe incluir:

- un volcado PostgreSQL realizado con `pg_dump`;
- el contenido del directorio `/opt/pami-data/media`;
- una copia cifrada y protegida del `.env`.

Las copias deben almacenarse también fuera del VPS y probarse mediante una restauración controlada. No basta con conservarlas en el mismo disco del servidor.

## Paso obligatorio para dominio y HTTPS

Cuando exista un dominio:

1. apuntar los registros DNS al VPS;
2. crear un bloque Nginx para el dominio en los puertos 80/443;
3. habilitar `443/tcp` en el firewall y obtener el certificado TLS;
4. actualizar `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` con el dominio y `https://`;
5. activar `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE` y `CSRF_COOKIE_SECURE`;
6. reconstruir los servicios y comprobar el proxy y el certificado;
7. retirar la publicación temporal del puerto `8025`;
8. mantener HSTS en `0` hasta verificar todo el portal por HTTPS;
9. activar HSTS gradualmente y evaluar subdominios/preload por separado.

## Recuperación básica

Ante un fallo de despliegue, revisar primero:

```bash
docker compose --env-file .env -f docker-compose.prod.yml ps
docker compose --env-file .env -f docker-compose.prod.yml logs --tail=200
```

No eliminar volúmenes ni directorios persistentes para intentar reparar un inicio fallido. Contienen la base de datos y los archivos subidos.
