from django.db import migrations


class Migration(migrations.Migration):
    """
    Elimina los modelos Wagtail deprecados:
    - nuestrosServicios (Orderable, FK a HomePage)
    - preguntasFrecuentes (Orderable, FK a HomePage)
    - HomePage (Wagtail Page subclass, reemplazada por LandingPage)
    """

    dependencies = [
        ('home', '0013_add_landing_seo_fields'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.DeleteModel(name='nuestrosServicios'),
        migrations.DeleteModel(name='preguntasFrecuentes'),
        migrations.DeleteModel(name='HomePage'),
    ]
