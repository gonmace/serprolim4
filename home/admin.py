from django.contrib import admin
from django.utils.html import format_html
from .models import LandingPage, LandingService, LandingFAQ

class ServiceInline(admin.TabularInline):
    model = LandingService
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
             return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.file.url)
        return ""
    image_preview.short_description = "Preview"

class FAQInline(admin.TabularInline):
    model = LandingFAQ
    extra = 1

@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'country', 'enabled']
    list_filter = ['country', 'enabled']
    inlines = [ServiceInline, FAQInline]
    
    readonly_fields = ['image_preview_bg', 'image_preview_main', 'image_preview_promo']

    fieldsets = (
        ("Configuration", {
            "fields": (
                "country",
                "enabled",
            ),
        }),
        ("Banner", {
            "fields": (
                "subtitle",
                "slogan",
                ("imageBG", "image_preview_bg"),
                ("imageMain", "image_preview_main"),
                ("imagePromo", "image_preview_promo"),
            ),
        }),
        ("Cotiza", {
            "fields": (
                "cotizaDescription",
                "mjeCotiza",
                "mjeFueraDeRango",
                "mjeWAContratando",
                "mjeWAFueraDeRango",
            ),
        }),
        ("Nuestros Servicios", {
            "fields": (
                "serviviosDescription",
                "displayNServicios",
            ),
        }),
    )

    def image_preview_bg(self, obj):
        if obj.imageBG:
             # Use proper storage or url access safely
             try:
                return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imageBG.file.url)
             except:
                return ""
        return ""
    image_preview_bg.short_description = "Preview"

    def image_preview_main(self, obj):
        if obj.imageMain:
            try:
                return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imageMain.file.url)
            except:
                return ""
        return ""
    image_preview_main.short_description = "Preview"

    def image_preview_promo(self, obj):
        if obj.imagePromo:
            try:
                return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imagePromo.file.url)
            except:
                return ""
        return ""
    image_preview_promo.short_description = "Preview"

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

