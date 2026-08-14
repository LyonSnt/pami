from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.site.urls")),
    path("", include("apps.businesses.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.portfolio.urls")),
    path("", include("apps.blog.urls")),
    path("", include("apps.contact.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
