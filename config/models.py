from django.db import models
from django.utils.translation import gettext_lazy as _


class CountrySettings(models.Model):
    """Settings for specific countries (e.g., Argentina, Paraguay, Bolivia)."""
    country_code = models.SlugField(
        max_length=5,
        unique=True,
        verbose_name=_('Country Code'),
        help_text=_('Unique code for the country (e.g., ar, py, bo)'),
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_('Country Name'),
        help_text=_('Name of the country (e.g., Argentina)'),
    )

    site_name = models.CharField(
        max_length=100,
        blank=True,
        default='MultiSane',
        verbose_name=_('Site Name'),
        help_text=_('Brand name for this country (overrides General Settings)'),
    )

    site_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Site URL'),
        help_text=_('Full canonical URL for this country (e.g., https://limpiezapozossepticos.com)'),
    )

    phone_prefix = models.CharField(
        max_length=5,
        default='591',
        verbose_name=_('Phone Prefix'),
        help_text=_('Country phone prefix (e.g., 54)'),
    )

    address = models.TextField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('Address'),
        help_text=_('Business address for this country'),
    )

    lat = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Latitude'),
    )

    lon = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Longitude'),
    )

    tel = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name=_('Phone'),
        help_text=_('Phone number for this country'),
    )

    cel = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name=_('WhatsApp / Celular 1'),
        help_text=_('WhatsApp number for this country'),
    )

    mjeGlobo = models.CharField(
        blank=True,
        null=True,
        max_length=128,
        verbose_name=_('WhatsApp Bubble Message'),
        help_text=_('Leave blank to hide WhatsApp bubble'),
    )

    cel2 = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name=_('Celular 2'),
        help_text=_('Secondary phone number'),
    )

    email = models.EmailField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('Email Address'),
        help_text=_('Contact email for this country'),
    )

    icon = models.FileField(
        upload_to='icons/',
        null=True,
        blank=True,
        verbose_name=_('Icon'),
        help_text=_('Website icon/logo for this country (SVG, PNG, JPG)'),
    )

    theme = models.CharField(
        max_length=50,
        choices=[
            ('serprolim', 'SerProLim (Amarillo/Verde)'),
            ('multisane', 'MultiSane (Emerald Green)'),
            ('limpio', 'Limpio (Compatible)'),
            ('limpio-ya', 'Limpio Ya (Logo Colors)'),
        ],
        default='multisane',
        verbose_name=_('Theme / Palette'),
        help_text=_('Select the color palette for this country'),
    )

    class Meta:
        db_table = 'wgeneraldata_countrysettings'  # Preserve table after app rename
        verbose_name = _('Country Settings')
        verbose_name_plural = _('Country Settings')
    
    # Social Media
    facebook = models.URLField(
        blank=True, 
        null=True, 
        help_text="facebook page"
    )
    instagram = models.URLField(
        blank=True, 
        null=True, 
        help_text="instagram"
    )
    tiktok = models.URLField(
        blank=True, 
        null=True, 
        help_text="tiktok"
    )
    youtube = models.URLField(
        blank=True, 
        null=True,
        help_text="youtube channel"
    )

    # Analytics: movido a app analytics (Project-level)

    # --- Landing Page Content Removed (Moved to home.LandingPage) ---

    def __str__(self):
        return f"{self.name} ({self.country_code})"

