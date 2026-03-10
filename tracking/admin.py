from django import forms
from django.contrib import admin

from .models import TrackingSettings


class TrackingSettingsForm(forms.ModelForm):
    """Form explícito con todos los campos para evitar filtrado del admin."""
    class Meta:
        model = TrackingSettings
        fields = '__all__'
        widgets = {
            'gtm': forms.Textarea(attrs={'rows': 3}),
            'google_analytics': forms.Textarea(attrs={'rows': 3}),
            'google_ads': forms.Textarea(attrs={'rows': 3}),
            'adsense': forms.Textarea(attrs={'rows': 3}),
            'fb_pixel': forms.Textarea(attrs={'rows': 3}),
            'open_graph': forms.Textarea(attrs={'rows': 3}),
            'head_scripts': forms.Textarea(attrs={'rows': 3}),
            'body_scripts': forms.Textarea(attrs={'rows': 3}),
        }


@admin.register(TrackingSettings)
class TrackingSettingsAdmin(admin.ModelAdmin):
    form = TrackingSettingsForm
    # Usar fields en lugar de fieldsets para evitar posibles bugs de renderizado
    fields = (
        'gtm', 'google_analytics', 'google_ads', 'adsense',
        'fb_pixel', 'open_graph', 'head_scripts', 'body_scripts',
    )

    def has_add_permission(self, request):
        return not TrackingSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
