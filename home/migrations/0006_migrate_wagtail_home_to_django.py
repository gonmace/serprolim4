from django.db import migrations

def copy_homepage_data(apps, schema_editor):
    HomePage = apps.get_model('home', 'HomePage')
    LandingPage = apps.get_model('home', 'LandingPage')
    LandingService = apps.get_model('home', 'LandingService')
    LandingFAQ = apps.get_model('home', 'LandingFAQ')
    
    # Get the last active homepage (or first, assuming singleton usage)
    # Using specific() is not available in migrations normally for Page models unless careful,
    # but we just need fields which are on the HomePage model itself.
    home_page = HomePage.objects.first()
    
    if not home_page:
        return

    # Create Landing Page
    landing = LandingPage.objects.create(
        subtitle=home_page.subtitle,
        slogan=home_page.slogan,
        imageBG_id=home_page.imageBG_id,
        imageMain_id=home_page.imageMain_id,
        imagePromo_id=home_page.imagePromo_id,
        
        cotizaDescription=home_page.cotizaDescription,
        mjeCotiza=home_page.mjeCotiza,
        mjeFueraDeRango=home_page.mjeFueraDeRango,
        mjeWAContratando=home_page.mjeWAContratando,
        mjeWAFueraDeRango=home_page.mjeWAFueraDeRango,
        
        serviviosDescription=home_page.serviviosDescription,
        displayNServicios=home_page.displayNServicios,
    )
    
    # Copy Services
    # We need to access the related manager. 
    # In migrations, related names might be available if the previous migration set them up.
    # checking original model definition: related_name='nuestros_servicios'
    
    for service in home_page.nuestros_servicios.all():
        LandingService.objects.create(
            landing_page=landing,
            image_id=service.image_id,
            titulo=service.titulo,
            resumen=service.resumen,
            sort_order=service.sort_order
        )

    # Copy FAQs
    for faq in home_page.preguntas_frecuentes.all():
        LandingFAQ.objects.create(
            landing_page=landing,
            pregunta=faq.pregunta,
            respuesta=faq.respuesta,
            display=faq.display,
            sort_order=faq.sort_order
        )

def reverse_copy(apps, schema_editor):
    LandingPage = apps.get_model('home', 'LandingPage')
    LandingPage.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_landingpage_landingfaq_landingservice'),
    ]

    operations = [
        migrations.RunPython(copy_homepage_data, reverse_copy),
    ]
