# Protección del acceso administrativo

El login en `/admin/` permanece accesible y exige una cuenta activa con acceso
staff. La visibilidad del formulario no concede acceso al CMS.

## Protección contra intentos fallidos

Pámi integra `django-axes==8.3.1` mediante su backend de control, middleware y
handler de base de datos. Los intentos y bloqueos se comparten entre procesos
Gunicorn mediante PostgreSQL y sobreviven a reinicios del servicio.

Valores iniciales, configurables desde el entorno:

```dotenv
ADMIN_LOGIN_FAILURE_LIMIT=5
ADMIN_LOGIN_COOLOFF_MINUTES=15
```

Ambos valores deben ser enteros positivos. Tras alcanzar el límite, se bloquea
temporalmente el nombre de usuario presentado, incluso con una contraseña
correcta. La respuesta es HTTP 429 y muestra un mensaje en español sin confirmar
si la cuenta existe. Incluye `Retry-After`, `Cache-Control: no-store, private`
y exclusión de indexación. El tiempo indicado en `Retry-After` es un máximo
conservador: 15 minutos con los valores iniciales.

Un login correcto antes de alcanzar el límite reinicia el contador. Los
intentos durante un bloqueo no prolongan su duración. Al finalizar el periodo,
se permite volver a intentar el acceso. No se cierran las sesiones existentes
ni se bloquea el portal público u otras cuentas.

Los fallos quedan registrados en los modelos de Axes, consultables por el
superusuario en el administrador. Se conservan hasta 100 registros individuales
de fallo por nombre de usuario. No se guardan contraseñas; los registros contienen
el usuario presentado, fecha, navegador, ruta e IP de conexión.

## Proxy e IP

El bloqueo se aplica por nombre de usuario, sin depender de IP, cookies o
User-Agent. Se silencia exclusivamente `axes.W006` porque recomienda incluir
la IP en el bloqueo: detrás de un proxy, la IP de conexión puede ser compartida
por todos los administradores. Las pruebas verifican que cambiar IP, navegador
o cookies no permite eludir el bloqueo del mismo nombre de usuario.

La IP registrada proviene de `REMOTE_ADDR`. No se confía en `X-Forwarded-For`;
en producción puede corresponder al proxy y no al visitante. Esta política no
limita ataques que prueban muchos nombres diferentes. El límite general por IP
requiere configuración adicional en el proxy del VPS. Una persona que conozca
un nombre de usuario puede provocar su bloqueo temporal; la recuperación no
depende de poder entrar al administrador.

## Recuperación

Esperar el periodo de bloqueo es suficiente. Para desbloquear una cuenta antes,
el responsable del servidor puede ejecutar:

```bash
docker compose --env-file .env -f docker-compose.prod.yml exec web python manage.py axes_reset_username NOMBRE_USUARIO
```

En desarrollo:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web python manage.py axes_reset_username NOMBRE_USUARIO
```

El comando elimina los contadores de esa cuenta, no el historial individual
de fallos. No se debe desactivar la protección para recuperar una cuenta.

## Instalación y alcance

La imagen actualizada debe reconstruirse para instalar la nueva dependencia.
Sus migraciones `axes` se aplican con `python manage.py migrate`, como parte
del arranque existente. El despliegue lo realiza el usuario.

Esta fase no añade segundo factor, acceso privado ni cambios de ruta. HTTPS,
cookies seguras y contraseñas fuertes siguen siendo necesarios en producción.

Referencias: [instalación de Axes](https://django-axes.readthedocs.io/en/stable/2_installation.html),
[configuración](https://django-axes.readthedocs.io/en/stable/4_configuration.html) y
[recuperación](https://django-axes.readthedocs.io/en/stable/3_usage.html).
