from django.core.exceptions import ValidationError


def validate_file_size(file, max_mb=5):
    max_size = max_mb * 1024 * 1024

    if file.size > max_size:
        raise ValidationError(f"El archivo no debe superar {max_mb} MB.")


def validate_image_extension(file):
    allowed_extensions = [".jpg", ".jpeg", ".png", ".webp"]

    file_name = file.name.lower()

    if not any(file_name.endswith(ext) for ext in allowed_extensions):
        raise ValidationError("Solo se permiten imágenes JPG, PNG o WEBP.")