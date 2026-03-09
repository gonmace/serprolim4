from django.db import migrations

def pivot_landing_page_to_country(apps, schema_editor):
    LandingPage = apps.get_model('home', 'LandingPage')
    CountrySettings = apps.get_model('generalData', 'CountrySettings')
    LandingService = apps.get_model('home', 'LandingService')
    LandingFAQ = apps.get_model('home', 'LandingFAQ')

    # Get Default Country (Bolivia) as fallback
    bo_settings = CountrySettings.objects.filter(country_code='bo').first()
    
    # Iterate over all landing pages
    for page in LandingPage.objects.all():
        # Determine target country
        target_country = page.country if page.country else bo_settings
        
        if not target_country:
            # Skip if no country exists at all (edge case)
            continue
            
        print(f"Migrating Landing Page {page.pk} to Country {target_country.name}")

        # 1. Copy Content Fields
        target_country.subtitle = page.subtitle
        target_country.slogan = page.slogan
        target_country.imageBG = page.imageBG
        target_country.imageMain = page.imageMain
        target_country.imagePromo = page.imagePromo
        
        target_country.cotizaDescription = page.cotizaDescription
        target_country.mjeCotiza = page.mjeCotiza
        target_country.mjeFueraDeRango = page.mjeFueraDeRango
        target_country.mjeWAContratando = page.mjeWAContratando
        target_country.mjeWAFueraDeRango = page.mjeWAFueraDeRango
        
        target_country.serviviosDescription = page.serviviosDescription
        target_country.displayNServicios = page.displayNServicios
        
        target_country.save()
        
        # 2. Re-parent Services
        # Update LandingService objects linked to this page
        LandingService.objects.filter(landing_page=page).update(country=target_country)
        
        # 3. Re-parent FAQs
        LandingFAQ.objects.filter(landing_page=page).update(country=target_country)


def reverse_pivot(apps, schema_editor):
    # This is destructive, we can't easily undo merging back into separate pages 
    # without logic to create pages. For now, we do nothing or could implement if needed.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_landingfaq_country_landingservice_country_and_more'),
        ('generalData', '0013_countrysettings_cotizadescription_and_more'), 
        # Added dependency on generalData because we write to CountrySettings
    ]

    operations = [
        migrations.RunPython(pivot_landing_page_to_country, reverse_pivot),
    ]
