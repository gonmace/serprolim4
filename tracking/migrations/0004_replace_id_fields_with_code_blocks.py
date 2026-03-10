from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Reemplaza los campos de ID individuales por textareas de código completo.
    Los campos head_scripts y body_scripts se conservan.
    """

    dependencies = [
        ('tracking', '0003_rename_and_add_fields'),
    ]

    operations = [
        # Eliminar campos de ID individuales
        migrations.RemoveField(model_name='trackingsettings', name='gtm_id'),
        migrations.RemoveField(model_name='trackingsettings', name='ga_g_tracking_id'),
        migrations.RemoveField(model_name='trackingsettings', name='gads_id'),
        migrations.RemoveField(model_name='trackingsettings', name='adsense_id'),
        migrations.RemoveField(model_name='trackingsettings', name='fb_pixel_id'),

        # Agregar textareas de código completo
        migrations.AddField(
            model_name='trackingsettings',
            name='gtm',
            field=models.TextField(blank=True, null=True, verbose_name='Google Tag Manager'),
        ),
        migrations.AddField(
            model_name='trackingsettings',
            name='google_analytics',
            field=models.TextField(blank=True, null=True, verbose_name='Google Analytics'),
        ),
        migrations.AddField(
            model_name='trackingsettings',
            name='google_ads',
            field=models.TextField(blank=True, null=True, verbose_name='Google Ads'),
        ),
        migrations.AddField(
            model_name='trackingsettings',
            name='adsense',
            field=models.TextField(blank=True, null=True, verbose_name='Google AdSense'),
        ),
        migrations.AddField(
            model_name='trackingsettings',
            name='fb_pixel',
            field=models.TextField(blank=True, null=True, verbose_name='Facebook / Meta Pixel'),
        ),
        migrations.AddField(
            model_name='trackingsettings',
            name='open_graph',
            field=models.TextField(blank=True, null=True, verbose_name='Open Graph'),
        ),
    ]
