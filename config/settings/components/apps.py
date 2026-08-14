DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # django_htmx
    # django_filters
    # django_extensions
]

LOCAL_APPS = [
    "apps.common.apps.CommonConfig",
    "apps.audit.apps.AuditConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.site.apps.SiteConfig",
    "apps.businesses.apps.BusinessesConfig",
    "apps.catalog.apps.CatalogConfig",
    "apps.portfolio.apps.PortfolioConfig",
    "apps.blog.apps.BlogConfig",
    "apps.contact.apps.ContactConfig",
]

INSTALLED_APPS = (
    DJANGO_APPS
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)
