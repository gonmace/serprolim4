from django.db import migrations

def reverse_pivot_landing_page(apps, schema_editor):
    CountrySettings = apps.get_model('generalData', 'CountrySettings')
    LandingPage = apps.get_model('home', 'LandingPage')
    LandingService = apps.get_model('home', 'LandingService')
    LandingFAQ = apps.get_model('home', 'LandingFAQ')

    # Iterate over all countries
    for country in CountrySettings.objects.all():
        print(f"Creating Landing Page for Country {country.name}")
        
        # Create LandingPage
        lp = LandingPage.objects.create(
            country=country,
            enabled=True, # Default to enabled as per requirement
            
            # Use 'getattr' with defaults to prevent errors if fields are missing/renamed in future schema, 
            # though they exist in current schema we are migrating from.
            subtitle=getattr(country, 'subtitle', ''),
            slogan=getattr(country, 'slogan', ''),
            imageBG=getattr(country, 'imageBG', None),
            imageMain=getattr(country, 'imageMain', None),
            imagePromo=getattr(country, 'imagePromo', None),
            
            cotizaDescription=getattr(country, 'cotizaDescription', ''),
            mjeCotiza=getattr(country, 'mjeCotiza', ''),
            mjeFueraDeRango=getattr(country, 'mjeFueraDeRango', ''),
            mjeWAContratando=getattr(country, 'mjeWAContratando', ''),
            mjeWAFueraDeRango=getattr(country, 'mjeWAFueraDeRango', ''),
            
            serviviosDescription=getattr(country, 'serviviosDescription', ''),
            displayNServicios=getattr(country, 'displayNServicios', True),
        )
        
        # Re-parent Services
        # Assuming 'country' FK on LandingService still holds the link
        updated_services = LandingService.objects.filter(country=country).update(landing_page=lp)
        print(f"  Moved {updated_services} services to LP {lp.id}")
        
        # Re-parent FAQs
        updated_faqs = LandingFAQ.objects.filter(country=country).update(landing_page=lp)
        print(f"  Moved {updated_faqs} FAQs to LP {lp.id}")


def reverse_reverse_pivot(apps, schema_editor):
    # If rolling back, we might lose the 'enabled' distinction or just disable them?
    # Logic to put data back into CountrySettings is complex and maybe not needed perfectly for rollback.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_landingpage_enabled_alter_landingfaq_country_and_more'), 
        ('generalData', '0013_countrysettings_cotizadescription_and_more'), 
    ]

    operations = [
        migrations.RunPython(reverse_pivot_landing_page, reverse_reverse_pivot),
    ]
