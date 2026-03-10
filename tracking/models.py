from django.db import models
from django.utils.translation import gettext_lazy as _


class TrackingSettings(models.Model):
    """
    Scripts de tracking y marketing inyectados en el <head>.
    Pegar el código completo que entrega cada plataforma.
    Singleton: solo existe una instancia.
    """

    gtm = models.TextField(
        blank=True, null=True,
        verbose_name=_('Google Tag Manager'),
        help_text=_('Pegar el snippet completo de GTM (incluye la etiqueta <script>)'),
    )
    google_analytics = models.TextField(
        blank=True, null=True,
        verbose_name=_('Google Analytics'),
        help_text=_('Snippet de GA4 — obtenido desde analytics.google.com'),
    )
    google_ads = models.TextField(
        blank=True, null=True,
        verbose_name=_('Google Ads'),
        help_text=_('Snippet de conversión de Google Ads'),
    )
    adsense = models.TextField(
        blank=True, null=True,
        verbose_name=_('Google AdSense'),
        help_text=_('Snippet de AdSense — obtenido desde adsense.google.com'),
    )
    fb_pixel = models.TextField(
        blank=True, null=True,
        verbose_name=_('Facebook / Meta Pixel'),
        help_text=_('Snippet completo del Pixel de Meta Ads (incluye el código base)'),
    )
    open_graph = models.TextField(
        blank=True, null=True,
        verbose_name=_('Open Graph (Facebook / WhatsApp / LinkedIn)'),
        help_text=_('Meta tags OG globales del sitio. Ej: og:image, og:site_name, fb:app_id'),
    )
    head_scripts = models.TextField(
        blank=True, null=True,
        verbose_name=_('Scripts adicionales en <head>'),
        help_text=_('Cualquier otro código HTML/JS a inyectar en el <head>'),
    )
    body_scripts = models.TextField(
        blank=True, null=True,
        verbose_name=_('Scripts adicionales en <body>'),
        help_text=_('Código HTML/JS a inyectar al cierre del <body>'),
    )

    class Meta:
        db_table = 'wanalytics_analyticssettings'
        verbose_name = _('Tracking & Marketing')
        verbose_name_plural = _('Tracking & Marketing')

    def __str__(self):
        return 'Tracking & Marketing'

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
