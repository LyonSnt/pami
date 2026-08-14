import unicodedata

from django.utils.text import slugify


def normalize_text(value: str) -> str:
    value = value or ""
    value = unicodedata.normalize("NFKD", value)
    return value.encode("ascii", "ignore").decode("ascii").strip()


def generate_slug(value: str) -> str:
    return slugify(normalize_text(value))