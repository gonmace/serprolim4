from django.contrib import admin

from .models import TrackingSettings


@admin.register(TrackingSettings)
class TrackingSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('HEAD', {
            'fields': ('head_scripts',),
            'description': 'AdSense, GTM, Meta Pixel, Open Graph... Todo lo que va en el <head>.',
        }),
        ('BODY', {
            'fields': ('body_scripts',),
            'description': 'GTM noscript, Meta Pixel noscript... Todo lo que va al inicio del <body>.',
        }),
    )

    def has_add_permission(self, request):
        return not TrackingSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
