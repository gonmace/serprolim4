from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _


class AnalyticsSettings(models.Model):
    """
    Tracking y analytics a nivel proyecto.
    GTM, gtag.js, scripts personalizados.
    """
    ga_g_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('G Tracking ID'),
        help_text=_('Google Analytics 4 (begins with "G-")'),
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
        help_text=_('Scripts entre las etiquetas <head>'),
    )
    body_scripts = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('<body> tracking scripts'),
        help_text=_('Scripts hacia el cierre de <body>'),
    )

    class Meta:
        db_table = 'wanalytics_analyticssettings'  # Mantener tabla existente tras renombrar app
        verbose_name = _('Analytics')
        verbose_name_plural = _('Analytics')

    def __str__(self):
        return 'Analytics'

    @classmethod
    def get_settings(cls):
        """Singleton: retorna la única instancia, crea si no existe."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
