from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gtm', models.TextField(blank=True, null=True, verbose_name='Google Tag Manager')),
                ('google_analytics', models.TextField(blank=True, null=True, verbose_name='Google Analytics')),
                ('google_ads', models.TextField(blank=True, null=True, verbose_name='Google Ads')),
                ('adsense', models.TextField(blank=True, null=True, verbose_name='Google AdSense')),
                ('fb_pixel', models.TextField(blank=True, null=True, verbose_name='Facebook / Meta Pixel')),
                ('open_graph', models.TextField(blank=True, null=True, verbose_name='Open Graph')),
                ('head_scripts', models.TextField(blank=True, null=True, verbose_name='Scripts adicionales en <head>')),
                ('body_scripts', models.TextField(blank=True, null=True, verbose_name='Scripts adicionales en <body>')),
            ],
            options={
                'verbose_name': 'Tracking & Marketing',
                'verbose_name_plural': 'Tracking & Marketing',
                'db_table': 'wanalytics_analyticssettings',
            },
        ),
    ]
