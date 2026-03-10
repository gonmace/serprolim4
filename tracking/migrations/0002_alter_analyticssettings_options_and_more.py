# Tabla ya existe como wanalytics_analyticssettings (de cuando el app era wanalytics)
# Solo actualizamos opciones y state; no tocamos la BD

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analyticssettings',
            options={'verbose_name': 'Analytics', 'verbose_name_plural': 'Analytics'},
        ),
        migrations.AlterField(
            model_name='analyticssettings',
            name='body_scripts',
            field=models.TextField(blank=True, help_text='Scripts hacia el cierre de <body>', null=True, verbose_name='<body> tracking scripts'),
        ),
        migrations.AlterField(
            model_name='analyticssettings',
            name='ga_g_tracking_id',
            field=models.CharField(blank=True, help_text='Google Analytics 4 (begins with "G-")', max_length=255, verbose_name='G Tracking ID'),
        ),
        migrations.AlterField(
            model_name='analyticssettings',
            name='head_scripts',
            field=models.TextField(blank=True, help_text='Scripts entre las etiquetas <head>', null=True, verbose_name='<head> tracking scripts'),
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterModelTable(
                    name='analyticssettings',
                    table='wanalytics_analyticssettings',
                ),
            ],
            database_operations=[],  # Tabla ya existe, no ejecutar ALTER
        ),
    ]
