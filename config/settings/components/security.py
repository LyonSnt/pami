from decouple import config

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="http://localhost:8025,http://127.0.0.1:8025",
).split(",")

SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", default=3600, cast=int)
SESSION_COOKIE_NAME = config("SESSION_COOKIE_NAME", default="pami_sessionid")
CSRF_COOKIE_NAME = config("CSRF_COOKIE_NAME", default="pami_csrftoken")

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)

X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True