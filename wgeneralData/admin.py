from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import GeneralSettings, Social, CountrySettings


# Register your models here.
# admin.site.register(CountrySettings) # This will be replaced by @admin.register

# Deprecated: GeneralSettings is now merged into CountrySettings (code='bo')
# admin.site.register(GeneralSettings)

# @admin.register(GeneralSettings)
# class GeneralSettingsAdmin(admin.ModelAdmin):
#     """
#     Django admin for GeneralSettings singleton model
#     """
#
#     readonly_fields = ('thumbnail',)
#
#     fieldsets = (
#         ('WhatsApp', {
#             'fields': ('cel', 'mjeGlobo'),
#             'description': 'WhatsApp contact configuration'
#         }),
#         ('General Contact Data', {
#             'fields': ('address', 'tel', 'cel2', 'email'),
#             'description': 'General business contact information'
#         }),
#         ('Branding', {
#             'fields': ('icon', 'thumbnail', 'theme'),
#             'description': 'Website branding assets'
#         }),
#         ('GPS Coordinates', {
#             'fields': ('lat', 'lon'),
#             'description': 'Location coordinates for maps'
#         }),
#     )
#
#     def thumbnail(self, obj):
#         if obj.icon:
#             # Added some styling to ensure visibility (especially for white SVGs)
#             return mark_safe(f'<div style="background-color: #004A7C; padding: 10px; display: inline-block; border-radius: 8px;"><img src="{obj.icon.url}" width="150" height="auto" alt="Logo Preview"/></div>')
#         return "No logo uploaded"
#     thumbnail.short_description = 'Logo Preview'
#
#     def has_add_permission(self, request):
#         """
#         Prevent adding more than one instance (singleton)
#         """
#         if GeneralSettings.objects.exists():
#             return False
#         return super().has_add_permission(request)
#
#     def has_delete_permission(self, request, obj=None):
#         """
#         Prevent deletion of the singleton instance
#         """
#         return False

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
        'fields': ('mjeGlobo', 'mjeWAContratando', 'mjeWAFueraDeRango'),
        'description': 'WhatsApp bubble configuration'
    }),
    ('Social Media', {
        'fields': ('facebook', 'instagram', 'tiktok', 'youtube'),
        'description': 'Social media links'
    }),
    ('Analytics', {
        'fields': ('ga_g_tracking_id', 'gtm_id', 'gads_id', 'head_scripts', 'body_scripts'),
        'description': 'Tracking codes'
    }),
    ('Maps', {
        'fields': ('lat', 'lon'),
        'description': 'Map coordinates and messages'
    }),
)

@admin.register(CountrySettings)
class CountrySettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code', 'phone_prefix', 'theme')

    # We define fieldsets above and use it here
    fieldsets = fieldsets
