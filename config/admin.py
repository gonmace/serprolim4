from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import GeneralSettings, Social, CountrySettings


fieldsets = (
    ('General Config', {
        'fields': ('country_code', 'name', 'phone_prefix'),
        'description': 'Basic country identification'
    }),
    ('Branding & Theme', {
        'fields': ('icon', 'theme'),
        'description': 'Visual appearance'
    }),
    ('Contact Info', {
        'fields': ('address', 'tel', 'cel', 'cel2', 'email'),
        'description': 'Contact details used in header/footer'
    }),
    ('WhatsApp Widget', {
        'fields': ('mjeGlobo',),
        'description': 'WhatsApp bubble configuration'
    }),
    ('Social Media', {
        'fields': ('facebook', 'instagram', 'tiktok', 'youtube'),
        'description': 'Social media links'
    }),
    ('Maps', {
        'fields': ('lat', 'lon'),
        'description': 'Map coordinates and messages'
    }),
)

THEME_CHOICES = [
    ('serprolim', 'SerProLim (Amarillo/Verde)'),
    ('multisane', 'MultiSane (Emerald Green)'),
    ('limpio', 'Limpio (Compatible)'),
    ('limpio-ya', 'Limpio Ya (Logo Colors)'),
]


@admin.register(CountrySettings)
class CountrySettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code', 'phone_prefix', 'theme')
    fieldsets = fieldsets

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'theme':
            kwargs['choices'] = THEME_CHOICES
        return super().formfield_for_dbfield(db_field, request, **kwargs)
