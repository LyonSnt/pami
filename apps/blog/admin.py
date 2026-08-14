from django.contrib import admin

from apps.audit.admin_mixins import AuditModelAdminMixin
from apps.blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("title", "business", "is_published", "published_at", "created_at")
    list_filter = ("business", "is_published", "published_at")
    search_fields = ("title", "slug", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("business",)
    date_hierarchy = "published_at"

    fieldsets = (
        ("Información general", {
            "fields": ("business", "title", "slug", "excerpt", "content")
        }),
        ("Imagen", {
            "fields": ("image",)
        }),
        ("Publicación", {
            "fields": ("is_published", "published_at")
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description")
        }),
    )
