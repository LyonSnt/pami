# Protección del acceso administrativo

El login exige una cuenta activa con acceso staff. Su ruta inicial es `/admin/`
y se puede cambiar desde el entorno. La visibilidad del formulario no concede
acceso al CMS.

## Ruta configurable

`ADMIN_URL_PATH` define el nombre de la ruta, con valor inicial `admin`:

```dotenv
ADMIN_URL_PATH=panel-pami
```

Con ese ejemplo el administrador se encuentra en `/panel-pami/` y el login en
`/panel-pami/login/`. Se permiten letras ASCII, números, guiones y guiones bajos;
las barras iniciales y finales son opcionales. No se permiten rutas anidadas,
valores vacíos ni nombres reservados para secciones públicas, static o media.

Después de editar el `.env`, recrear el servicio para cargar el valor nuevo:

```bash
docker compose --env-file .env -f docker-compose.prod.yml up -d --build --force-recreate web
```

No requiere migraciones adicionales. Todos los enlaces administrativos usan
el namespace `admin` de Django y siguen la nueva ruta. El modo mantenimiento
permite acceder al administrador configurado y el bloqueo de Axes permanece
activo. Cuando se utiliza otro nombre, `/admin`, `/admin/` y sus subrutas
responden con una página institucional propia, HTTP 404, sin redirigir ni revelar la ruta nueva,
tanto con `DEBUG=True` como con `DEBUG=False`. Esta respuesta también se
mantiene durante el mantenimiento. Los demás errores inesperados de desarrollo
conservan el diagnóstico técnico de Django.

La página de la ruta antigua muestra `Página no disponible` y
`Esta dirección no está disponible. Puedes volver al inicio para continuar.`,
con un único botón `Volver al inicio`. No incluye búsqueda ni mensajes de
acceso restringido. El 404 general y el de módulos desactivados conservan
su texto y sus acciones habituales.

`robots.txt` no enumera la ruta administrativa para evitar publicarla; las
páginas del administrador mantienen su metadato de exclusión de indexación.
Los archivos `/static/admin/` conservan su ruta habitual: son recursos de CSS
y JavaScript, no el acceso al CMS.

Cambiar el nombre reduce visitas automatizadas a la ruta conocida, pero no
reemplaza autenticación, límites de intentos ni HTTPS. Si existen reglas del
proxy específicas para `/admin/`, el responsable del despliegue debe ajustarlas
al nombre elegido. Las reglas de proxy genéricas del proyecto siguen funcionando.

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

## Segundo factor: mejora recomendada y pospuesta

El 7 de octubre de 2026 el usuario decidió dejar documentado el análisis
del segundo factor y posponer su implementación. No está instalado ni activo,
no es un requisito funcional para usar Pámi y no hay autorización vigente
para implementarlo. Debe retomarse como un alcance nuevo aprobado por el usuario.

Los controles actuales incluyen contraseña, permisos por roles, bloqueo de
intentos con Axes, auditoría y ruta configurable. HTTPS y cookies seguras
deben mantenerse correctamente configurados en el VPS. Estos controles no
impiden que alguien que obtenga la contraseña correcta pueda iniciar sesión.
Por eso se recomienda un segundo factor para el administrador público,
especialmente para el superusuario, que gestiona cuentas y puede descargar
respaldos de la base de datos. Cambiar la ruta no reemplaza esta protección.

Alcance propuesto para una futura implementación:

- Contraseña seguida de un código temporal de seis dígitos generado por una
  aplicación autenticadora (TOTP).
- Configuración por usuario mediante QR y confirmación de un código antes de
  activar el dispositivo.
- Exigencia de verificación para todas las cuentas administrativas, incluidos
  superusuarios, protegiendo todas las vistas del CMS y las sesiones anteriores.
- Códigos de recuperación de un solo uso y procedimiento de recuperación
  desde el VPS si se pierde el teléfono y los códigos.
- Pantallas en español bajo la ruta configurada mediante `ADMIN_URL_PATH`.
- Conservación del bloqueo de contraseñas y límites para los errores del
  segundo factor, comprobando su integración con Axes.
- Activación controlada que permita configurar el dispositivo antes de exigir
  el segundo factor, evitando perder el acceso al único administrador.

Se evaluó `django-two-factor-auth` sobre `django-otp` como posible solución;
las dependencias y su compatibilidad deberán verificarse nuevamente al retomar.
El paquete no hace obligatoria por sí solo la configuración del segundo
factor: habría que implementar y probar esa política para Pámi.

La modalidad propuesta no requiere una suscripción externa ni cobros por
código. Se ejecutaría en el VPS actual dentro de Docker, con dependencias
incluidas en la imagen y migraciones aplicadas en el arranque. Cada
administrador necesitaría una aplicación autenticadora en su teléfono,
guardar los códigos de recuperación por separado y mantener la hora del
teléfono y servidor sincronizada. No se propone SMS, llamadas ni correo como
segundo factor. Las obligaciones de mantener y actualizar la aplicación y
el VPS continúan vigentes.

Antes de habilitarlo en producción se deben validar en desarrollo el alta
del dispositivo, acceso sin verificación, códigos incorrectos y reutilizados,
expiración, bloqueo, recuperación y revocación de sesiones. El despliegue lo
realiza el usuario después de aprobar el resultado y autorizar el commit.

Mientras se pospone, mantener contraseña larga y única, acceso administrativo
limitado a las cuentas necesarias, HTTPS, cookies seguras y respaldos.

Referencias: [recomendaciones de MFA de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html),
[política de acceso de Django Two-Factor Authentication](https://django-two-factor-auth.readthedocs.io/en/stable/implementing.html) y
[licencia del proyecto](https://github.com/jazzband/django-two-factor-auth/blob/master/LICENSE).

## Instalación y alcance

La imagen actualizada debe reconstruirse para instalar la nueva dependencia.
Sus migraciones `axes` se aplican con `python manage.py migrate`, como parte
del arranque existente. El despliegue lo realiza el usuario.

Esta fase no añade segundo factor ni acceso privado. HTTPS,
cookies seguras y contraseñas fuertes siguen siendo necesarios en producción.

Referencias: [instalación de Axes](https://django-axes.readthedocs.io/en/stable/2_installation.html),
[configuración](https://django-axes.readthedocs.io/en/stable/4_configuration.html) y
[recuperación](https://django-axes.readthedocs.io/en/stable/3_usage.html).
