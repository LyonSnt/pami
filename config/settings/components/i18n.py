from decouple import config

LANGUAGE_CODE = config("LANGUAGE_CODE", default="es-ec")
TIME_ZONE = config("TIME_ZONE", default="America/Guayaquil")

USE_I18N = True
USE_TZ = True