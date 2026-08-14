from django.contrib import admin

from apps.audit.admin_mixins import AuditModelAdminMixin
from apps.catalog.models import Product


@admin.register(Product)
class ProductAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("name", "business", "price", "show_price", "order", "is_published", "created_at")
    list_filter = ("business", "show_price", "is_published")
    search_fields = ("name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("business",)

    fieldsets = (
        ("Información general", {
            "fields": ("business", "name", "slug", "short_description", "description")
        }),
        ("Imagen", {
            "fields": ("image",)
        }),
        ("Precio", {
            "fields": ("price", "show_price")
        }),
        ("Publicación", {
            "fields": ("order", "is_published")
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description")
        }),
    )
