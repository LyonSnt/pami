from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from PIL import ImageOps


WEBP_OPTIONS = {"quality": 82}


class ExifOrientation:
    """Apply camera orientation to pixels and remove the obsolete EXIF flag."""

    def process(self, image):
        return ImageOps.exif_transpose(image)


def responsive_image_spec(*, width, height, source="image"):
    return ImageSpecField(
        source=source,
        processors=[ExifOrientation(), ResizeToFill(width, height)],
        format="WEBP",
        options=WEBP_OPTIONS,
    )
