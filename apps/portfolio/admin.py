from django.contrib import admin

from apps.audit.admin_mixins import AuditModelAdminMixin
from apps.portfolio.models import PortfolioProject


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("title", "business", "client_name", "project_date", "order", "is_active", "is_published", "created_at")
    list_filter = ("business", "is_active", "is_published", "project_date")
    search_fields = ("title", "slug", "short_description", "client_name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("business",)

    fieldsets = (
        ("Información general", {
            "fields": ("business", "title", "slug", "short_description", "description")
        }),
        ("Imagen", {
            "fields": ("image",)
        }),
        ("Datos del proyecto", {
            "fields": ("client_name", "project_date")
        }),
        ("Publicación", {
            "fields": ("order", "is_active", "is_published")
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description")
        }),
    )
