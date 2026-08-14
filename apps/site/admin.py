from django.contrib import admin

from apps.audit.admin_mixins import AuditModelAdminMixin
from apps.site.models import NavigationItem, SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("site_name", "email", "phone", "whatsapp", "maintenance_mode", "created_at")
    search_fields = ("site_name", "email", "phone", "whatsapp")
    list_filter = ("maintenance_mode",)

    fieldsets = (
        ("Información general", {
            "fields": ("site_name", "slogan", "description")
        }),
        (
            "Hero principal",
            {
                "fields": (
                    "hero_title",
                    "hero_description",
                    "hero_primary_button_text",
                    "hero_primary_button_url",
                    "hero_secondary_button_text",
                    "hero_secondary_button_url",
                    "hero_image",
                )
            },
        ),
        ("Identidad visual", {
            "fields": ("logo", "favicon")
        }),
        ("Contacto", {
            "fields": ("email", "phone", "whatsapp", "address")
        }),
        ("Redes sociales", {
            "fields": (
                "facebook_url",
                "instagram_url",
                "tiktok_url",
                "youtube_url",
                "linkedin_url",
            )
        }),
        ("SEO", {
            "fields": ("seo_title", "seo_description")
        }),
        ("Estado", {
            "fields": ("maintenance_mode",)
        }),
    )

    def has_add_permission(self, request):
        if SiteConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(NavigationItem)
class NavigationItemAdmin(AuditModelAdminMixin, admin.ModelAdmin):
    list_display = ("label", "url", "order", "is_active", "open_in_new_tab")
    list_filter = ("is_active", "open_in_new_tab")
    search_fields = ("label", "url")
    ordering = ("order", "label")
