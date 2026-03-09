from django.contrib import admin
from .models import AnalyticsSettings


@admin.register(AnalyticsSettings)
class AnalyticsSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Google Tag Manager (GTM)', {
            'fields': ('gtm_id',),
            'description': 'ID comienza con "GTM-"'
        }),
        ('Global site tag (gtag.js)', {
            'fields': ('ga_g_tracking_id', 'gads_id'),
            'description': 'Google Analytics 4 (G-) y Google Ads (AW-)'
        }),
        ('Scripts adicionales', {
            'fields': ('head_scripts', 'body_scripts'),
        }),
    )

    def has_add_permission(self, request):
        return not AnalyticsSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
