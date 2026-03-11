from django.db import migrations

SERVICIOS = [
    {
        "titulo": "Pozos Ciegos",
        "resumen": "Limpieza y vaciado completo de pozos ciegos residenciales e industriales. Equipo con bombas de vacío de alta presión para una extracción eficiente.",
        "sort_order": 1,
    },
    {
        "titulo": "Cámaras Sépticas",
        "resumen": "Succión y limpieza de cámaras sépticas con transporte y disposición final de lodos conforme a normativas ambientales.",
        "sort_order": 2,
    },
    {
        "titulo": "Destranque Tuberías",
        "resumen": "Desobstrucción de tuberías, baños, cocinas y alcantarillado domiciliar e industrial con equipamiento especializado.",
        "sort_order": 3,
    },
    {
        "titulo": "Aguas Residuales",
        "resumen": "Evacuación, transporte y disposición responsable de aguas residuales y aguas grises para condominios, industrias y urbanizaciones.",
        "sort_order": 4,
    },
    {
        "titulo": "Servicio Industrial",
        "resumen": "Limpieza de cámaras de separación, trampas de grasa, tanques industriales y manejo especializado de condensados y lodo empetrolado.",
        "sort_order": 5,
    },
    {
        "titulo": "Construcción Pozos",
        "resumen": "Construcción, refacción y mejora de pozos ciegos y cámaras sépticas. Soluciones duraderas para hogares, empresas y urbanizaciones.",
        "sort_order": 6,
    },
]


def seed_services(apps, schema_editor):
    LandingPage = apps.get_model("home", "LandingPage")
    LandingService = apps.get_model("home", "LandingService")

    # Attach to the first enabled landing page, or the first one available
    landing = LandingPage.objects.filter(enabled=True).first()
    if not landing:
        landing = LandingPage.objects.first()
    if not landing:
        return  # Nothing to attach to

    # Skip if services already exist for this landing page
    if LandingService.objects.filter(landing_page=landing).exists():
        return

    for s in SERVICIOS:
        LandingService.objects.create(
            landing_page=landing,
            titulo=s["titulo"],
            resumen=s["resumen"],
            sort_order=s["sort_order"],
        )


def unseed_services(apps, schema_editor):
    LandingService = apps.get_model("home", "LandingService")
    LandingService.objects.filter(titulo__in=[s["titulo"] for s in SERVICIOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0017_homepage_nuestrosservicios_preguntasfrecuentes"),
    ]

    operations = [
        migrations.RunPython(seed_services, unseed_services),
    ]
