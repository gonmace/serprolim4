from django.db import migrations

def copy_general_to_country(apps, schema_editor):
    GeneralSettings = apps.get_model('generalData', 'GeneralSettings')
    CountrySettings = apps.get_model('generalData', 'CountrySettings')

    # Get the singleton GeneralSettings instance
    general_settings = GeneralSettings.objects.first()

    if general_settings:
        # Create a new CountrySettings for Bolivia (Default)
        CountrySettings.objects.create(
            country_code='bo',
            name='Bolivia',
            phone_prefix=general_settings.phone_prefix,
            address=general_settings.address,
            lat=general_settings.lat,
            lon=general_settings.lon,
            tel=general_settings.tel,
            cel=general_settings.cel,
            mjeGlobo=general_settings.mjeGlobo,
            cel2=general_settings.cel2,
            email=general_settings.email,
            # For FileField (icon), we just copy the reference. 
            # Note: This points to the same file on disk.
            icon=general_settings.icon,
            theme=general_settings.theme,
        )

def reverse_func(apps, schema_editor):
    CountrySettings = apps.get_model('generalData', 'CountrySettings')
    CountrySettings.objects.filter(country_code='bo').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('generalData', '0009_countrysettings_generalsettings_phone_prefix'),
    ]

    operations = [
        migrations.RunPython(copy_general_to_country, reverse_func),
    ]
