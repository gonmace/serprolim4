"""Simplifica TrackingSettings a solo head_scripts y body_scripts."""
from django.db import migrations, models


def migrate_data(apps, schema_editor):
    """Combina todos los campos en head_scripts y body_scripts."""
    TrackingSettings = apps.get_model('tracking', 'TrackingSettings')
    try:
        obj = TrackingSettings.objects.get(pk=1)
        parts = []
        for field in ['open_graph', 'gtm', 'adsense', 'fb_pixel', 'head_scripts']:
            val = getattr(obj, field, None) or ''
            if val.strip():
                parts.append(val.strip())
        obj.head_scripts = '\n\n'.join(parts) if parts else ''
        obj.body_scripts = (obj.body_scripts or '').strip()
        obj.save()
    except TrackingSettings.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_alter_trackingsettings_adsense_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_data, migrations.RunPython.noop),
        migrations.RemoveField(model_name='trackingsettings', name='adsense'),
        migrations.RemoveField(model_name='trackingsettings', name='fb_pixel'),
        migrations.RemoveField(model_name='trackingsettings', name='google_ads'),
        migrations.RemoveField(model_name='trackingsettings', name='google_analytics'),
        migrations.RemoveField(model_name='trackingsettings', name='gtm'),
        migrations.RemoveField(model_name='trackingsettings', name='open_graph'),
        migrations.AlterField(
            model_name='trackingsettings',
            name='head_scripts',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Scripts en <head>',
                help_text='Todo el código a inyectar en el <head>: AdSense, GTM, Meta Pixel, Open Graph, etc. Pegar el HTML completo con sus comentarios.',
            ),
        ),
        migrations.AlterField(
            model_name='trackingsettings',
            name='body_scripts',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Scripts en <body>',
                help_text='Código a inyectar al inicio del <body>: GTM noscript, Meta Pixel noscript, etc. Pegar el HTML completo con sus comentarios.',
            ),
        ),
    ]
