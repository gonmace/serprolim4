from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)

from wagtail.contrib.settings.models import BaseGenericSetting, register_setting

# @register_setting(icon='facebook')
class Social(BaseGenericSetting):

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

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("instagram"),
            FieldPanel("tiktok"),
            FieldPanel("youtube"),
        ], heading="Social Media Settings"),
    ]


# New Django Model (no longer Wagtail)
class GeneralSettings(models.Model):
    """
    Singleton model for general site settings.
    Only one instance should exist.
    """

    address = models.TextField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('Address'),
        help_text=_('Business address'),
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
        max_length=12,
        verbose_name=_('Phone'),
        help_text=_('Phone number (e.g., 3215779)'),
    )

    cel = models.CharField(
        blank=True,
        null=True,
        max_length=12,
        verbose_name=_('WhatsApp / Celular 1'),
        help_text=_('WhatsApp number (e.g., 76644033)'),
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
        max_length=12,
        verbose_name=_('Celular 2'),
        help_text=_('Secondary phone number'),
    )


    email = models.EmailField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('Email Address'),
        help_text=_('Contact email (e.g., serprolim@limpiezapozossepticos.com)'),
    )

    icon = models.FileField(
        upload_to='icons/',
        null=True,
        blank=True,
        verbose_name=_('Icon'),
        help_text=_('Website icon/logo (SVG, PNG, JPG)'),
    )


    phone_prefix = models.CharField(
        max_length=5,
        default='591',
        verbose_name=_('Phone Prefix'),
        help_text=_('Country phone prefix (e.g., 591)'),
    )

    theme = models.CharField(
        max_length=50,
        choices=[
            ('serprolim', 'Serprolim (Original)'),
            ('limpio', 'Limpio (Compatible)'),
            ('limpio-ya', 'Limpio Ya (Logo Colors)'),
            ('multisane', 'MultiSane (Emerald Green)'),
        ],
        default='serprolim',
        verbose_name=_('Theme / Palette'),
        help_text=_('Select the color palette for the site'),
    )

    class Meta:
        verbose_name = _('General Settings')
        verbose_name_plural = _('General Settings')

    def __str__(self):
        return "General Settings"

    def save(self, *args, **kwargs):
        """
        Singleton pattern: ensure only one instance exists
        """
        if not self.pk and GeneralSettings.objects.exists():
            raise ValidationError('Only one GeneralSettings instance is allowed')
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load the singleton instance, create if doesn't exist
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class CountrySettings(models.Model):
    """
    Settings for specific countries (e.g., Argentina, Paraguay).
    Overrides GeneralSettings when selected.
    """
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
            ('serprolim', 'Serprolim (Original)'),
            ('limpio', 'Limpio (Compatible)'),
            ('limpio-ya', 'Limpio Ya (Logo Colors)'),
            ('multisane', 'MultiSane (Emerald Green)'),
        ],
        default='serprolim',
        verbose_name=_('Theme / Palette'),
        help_text=_('Select the color palette for this country'),
    )

    class Meta:
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

    # Analytics
    ga_g_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('G Tracking ID'),
        help_text=_('Your Google Analytics 4 tracking ID (begins with "G-")'),
    )
    gtm_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Google Tag Manager ID'),
        help_text=_('Begins with "GTM-"'),
    )
    gads_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Google Ads ID'),
        help_text=_('Begins with "AW-"'),
    )
    head_scripts = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('<head> tracking scripts'),
        help_text=_('Add tracking scripts between the <head> tags.'),
    )
    body_scripts = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('<body> tracking scripts'),
        help_text=_('Add tracking scripts toward closing <body> tag.'),
    )

    # --- Landing Page Content Removed (Moved to home.LandingPage) ---

    def __str__(self):
        return f"{self.name} ({self.country_code})"

