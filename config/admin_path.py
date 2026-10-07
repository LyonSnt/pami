import re

from django.core.exceptions import ImproperlyConfigured


def normalize_admin_path(value):
    name = value.strip().strip("/")
    reserved = {"buscar", "catalogo", "negocios", "portafolio", "blog", "contacto", "static", "media"}
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name) or name.lower() in reserved:
        raise ImproperlyConfigured(
            "ADMIN_URL_PATH debe ser un nombre simple con letras, números, guiones o "
            "guiones bajos, sin coincidir con rutas públicas, static o media."
        )
    return name + "/"
