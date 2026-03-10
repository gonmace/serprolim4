from django.db import migrations

def copy_pivot_data(apps, schema_editor):
    CountrySettings = apps.get_model('config', 'CountrySettings')
    Social = apps.get_model('config', 'Social')
    # Analytics settings are in analytics app
    try:
        AnalyticsSettings = apps.get_model('tracking', 'AnalyticsSettings')
    except LookupError:
        AnalyticsSettings = None

    # Get the default country (Bolivia/Global)
    bo_settings = CountrySettings.objects.filter(country_code='bo').first()
    
    if bo_settings:
        # Copy Social Data
        social = Social.objects.first()
        if social:
            bo_settings.facebook = social.facebook
            bo_settings.instagram = social.instagram
            bo_settings.tiktok = social.tiktok
            bo_settings.youtube = social.youtube
        
        # Copy Analytics Data
        if AnalyticsSettings:
            analytics = AnalyticsSettings.objects.first()
            if analytics:
                bo_settings.ga_g_tracking_id = analytics.ga_g_tracking_id
                bo_settings.gtm_id = analytics.gtm_id
                bo_settings.gads_id = analytics.gads_id
                bo_settings.head_scripts = analytics.head_scripts
                bo_settings.body_scripts = analytics.body_scripts
        
        bo_settings.save()

class Migration(migrations.Migration):

    dependencies = [
        ('config', '0011_countrysettings_body_scripts_and_more'),
        # Ensure wanalytics migration is run if possible, though we access via get_model
    ]

    operations = [
        migrations.RunPython(copy_pivot_data, migrations.RunPython.noop),
    ]
