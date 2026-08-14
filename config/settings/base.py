from decouple import config

from .components.base import BASE_DIR

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1"
).split(",")

ROOT_URLCONF = "config.urls.public"
WSGI_APPLICATION = "config.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from .components.apps import *
from .components.auth import *
from .components.cache import *
from .components.database import *
from .components.email import *
from .components.i18n import *
from .components.logging import *
from .components.middleware import *
from .components.security import *
from .components.static import *
from .components.templates import *