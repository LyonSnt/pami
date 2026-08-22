from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


WEBP_OPTIONS = {"quality": 82}


def responsive_image_spec(*, width, height, source="image"):
    return ImageSpecField(
        source=source,
        processors=[ResizeToFill(width, height)],
        format="WEBP",
        options=WEBP_OPTIONS,
    )
