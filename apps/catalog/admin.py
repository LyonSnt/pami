from django.contrib import admin

from apps.audit.admin_mixins import AuditModelAdminMixin
from apps.catalog.models import Product, ProductFeature, ProductImage


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0
    fields = ("title", "description", "order", "is_active")
    ordering = ("order", "title")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ("image", "alt_text", "order", "is_active")
    ordering = ("order", "created_at")


@admin.register(Product)
class ProductAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("name", "business", "commercial_status", "price", "show_price", "order", "is_active", "is_published", "created_at")
    list_filter = ("business", "commercial_status", "show_price", "is_active", "is_published")
    search_fields = ("name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("business",)
    inlines = (ProductFeatureInline, ProductImageInline)

    fieldsets = (
        ("Información general", {
            "fields": (
                "business",
                "name",
                "slug",
                "short_description",
                "description",
                "target_audience",
                "additional_information",
                "demo_url",
            )
        }),
        ("Imagen", {
            "fields": ("image",)
        }),
        ("Precio", {
            "fields": ("commercial_status", "price", "show_price")
        }),
        ("Publicación", {
            "fields": ("order", "is_active", "is_published")
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description")
        }),
    )


@admin.register(ProductFeature)
class ProductFeatureAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("title", "product", "order", "is_active")
    list_filter = ("is_active", "product__business")
    search_fields = ("title", "description", "product__name")
    autocomplete_fields = ("product",)
    ordering = ("product", "order", "title")


@admin.register(ProductImage)
class ProductImageAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "product", "order", "is_active")
    list_filter = ("is_active", "product__business")
    search_fields = ("alt_text", "product__name")
    autocomplete_fields = ("product",)
    ordering = ("product", "order", "created_at")
