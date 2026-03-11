from django.db import models
from django.utils.translation import gettext_lazy as _


class TrackingSettings(models.Model):
    """
    Scripts de tracking y marketing.
    Singleton: solo existe una instancia.
    """

    head_scripts = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Scripts en <head>'),
        help_text=_('Todo el código a inyectar en el <head>: AdSense, GTM, Meta Pixel, Open Graph, etc. Pegar el HTML completo con sus comentarios.'),
    )
    body_scripts = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Scripts en <body>'),
        help_text=_('Código a inyectar al inicio del <body>: GTM noscript, Meta Pixel noscript, etc. Pegar el HTML completo con sus comentarios.'),
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
