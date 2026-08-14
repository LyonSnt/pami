from django.contrib import admin

from apps.audit.admin_mixins import AuditModelAdminMixin
from apps.businesses.models import Business


@admin.register(Business)
class BusinessAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ("Información general", {
            "fields": ("name", "slug", "short_description", "description")
        }),
        ("Identidad visual", {
            "fields": ("image", "icon")
        }),
        ("Publicación", {
            "fields": ("order", "is_published")
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description")
        }),
    )
