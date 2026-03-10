from django.db import migrations, models


class Migration(migrations.Migration):
    """
    - Renombra AnalyticsSettings → TrackingSettings en el estado de migraciones
    - Agrega campos: adsense_id, fb_pixel_id
    - La tabla DB (wanalytics_analyticssettings) se preserva sin cambios
    """

    dependencies = [
        ('tracking', '0002_alter_analyticssettings_options_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameModel(
                    old_name='AnalyticsSettings',
                    new_name='TrackingSettings',
                ),
            ],
            database_operations=[],  # La tabla ya existe, no renombrar
        ),
        migrations.AddField(
            model_name='trackingsettings',
            name='adsense_id',
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name='Google AdSense ID',
                help_text='Comienza con "ca-pub-"',
            ),
        ),
        migrations.AddField(
            model_name='trackingsettings',
            name='fb_pixel_id',
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name='Facebook / Meta Pixel ID',
                help_text='ID numérico del Pixel de Meta Ads',
            ),
        ),
    ]
