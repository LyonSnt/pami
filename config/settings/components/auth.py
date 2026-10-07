from datetime import timedelta

from decouple import config
from django.core.exceptions import ImproperlyConfigured

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Database tracking is shared by every Gunicorn worker and survives restarts.
AXES_HANDLER = "axes.handlers.database.AxesDatabaseHandler"
AXES_FAILURE_LIMIT = config("ADMIN_LOGIN_FAILURE_LIMIT", default=5, cast=int)
ADMIN_LOGIN_COOLOFF_MINUTES = config("ADMIN_LOGIN_COOLOFF_MINUTES", default=15, cast=int)
if AXES_FAILURE_LIMIT < 1 or ADMIN_LOGIN_COOLOFF_MINUTES < 1:
    raise ImproperlyConfigured("Los límites del login administrativo deben ser positivos.")
AXES_COOLOFF_TIME = timedelta(minutes=ADMIN_LOGIN_COOLOFF_MINUTES)
AXES_ONLY_ADMIN_SITE = True
AXES_LOCKOUT_PARAMETERS = ["username"]
# A reverse proxy can be the connection IP for every administrator. Block the
# submitted username across IPs instead; test changing cookies/User-Agent/IP.
# IP-wide spraying limits belong at the trusted proxy, configured on the VPS.
SILENCED_SYSTEM_CHECKS = ["axes.W006"]
AXES_RESET_ON_SUCCESS = True
AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = False
AXES_ENABLE_ACCESS_FAILURE_LOG = True
AXES_ACCESS_FAILURE_LOG_PER_USER_LIMIT = 100
AXES_CLIENT_IP_CALLABLE = "apps.accounts.security.get_connection_ip"
AXES_LOCKOUT_CALLABLE = "apps.accounts.security.admin_lockout_response"
