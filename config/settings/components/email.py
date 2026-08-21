from decouple import config

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="Pámi <no-reply@pami.local>",
)

EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
EMAIL_TIMEOUT = config("EMAIL_TIMEOUT", default=10, cast=int)

CONTACT_NOTIFICATION_EMAIL = config("CONTACT_NOTIFICATION_EMAIL", default="")
CONTACT_DUPLICATE_WINDOW_SECONDS = config(
    "CONTACT_DUPLICATE_WINDOW_SECONDS",
    default=60,
    cast=int,
)
CONTACT_RATE_LIMIT_MAX_SUBMISSIONS = config(
    "CONTACT_RATE_LIMIT_MAX_SUBMISSIONS",
    default=5,
    cast=int,
)
CONTACT_RATE_LIMIT_WINDOW_SECONDS = config(
    "CONTACT_RATE_LIMIT_WINDOW_SECONDS",
    default=600,
    cast=int,
)
