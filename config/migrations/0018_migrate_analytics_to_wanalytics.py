# Migración manual: copiar analytics de Bolivia a wanalytics, luego eliminar de CountrySettings

from django.db import migrations


def copy_analytics_to_wanalytics(apps, schema_editor):
    CountrySettings = apps.get_model('config', 'CountrySettings')
    AnalyticsSettings = apps.get_model('tracking', 'AnalyticsSettings')
    bo = CountrySettings.objects.filter(country_code='bo').first()
    if not bo:
        return
    settings, _ = AnalyticsSettings.objects.get_or_create(pk=1)
    settings.ga_g_tracking_id = bo.ga_g_tracking_id or ''
    settings.gtm_id = bo.gtm_id or ''
    settings.gads_id = bo.gads_id or ''
    settings.head_scripts = bo.head_scripts or ''
    settings.body_scripts = bo.body_scripts or ''
    settings.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('config', '0017_migrate_analytics_to_wanalytics'),
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_analytics_to_wanalytics, noop),
    ]
