from django.db import models
from django.core.cache import cache

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)

from wmetadata.models import MetadataPageMixin

class HomePage(MetadataPageMixin, Page):

    subpage_types = [
        'blog.BlogIndexPage',
        'base.StandardPage'
    ]
# BANNER
    subtitle = models.CharField(
        "Sub Titulo",
        max_length=50,
        blank=True,
        null=True,
        help_text="Subitulo",
        )
    slogan = models.TextField(
        "Slogan",
        blank=True,
        null=True,
        help_text="Slogan",
        )
    imageBG = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    imageMain = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    imagePromo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
# COTIZA
    cotizaDescription = models.TextField(
        "Descripcion",
        max_length=350,
        blank=True,
        null=True,
        help_text="Descripcion Cotizar",
        )
    mjeCotiza = models.CharField(
        "Cotiza",
        max_length=200,
        blank=True,
        null=True,
        help_text="Mensaje de Cotiza una que se selecciona el lugar",
        )
    mjeFueraDeRango = models.CharField(
        "Fuera de Rango",
        max_length=200,
        blank=True,
        null=True,
        help_text="La posición esta fuera del rango que se tiene en los mapas",
        )
    mjeWAContratando = models.CharField(
        "Whatsapp Contratando",
        max_length=200,
        blank=True,
        null=True,
        help_text="Mensaje Whatsapp Contratando servicio",
        )
    mjeWAFueraDeRango = models.CharField(
        "Whatsapp Fuera de rango",
        max_length=200,
        blank=True,
        null=True,
        help_text="Mensaje Whatsapp fuera de rango",
        )
# NUESTROS SERVICIOS
    serviviosDescription = models.TextField(
        "Servicios",
        max_length=350,
        blank=True,
        null=True,
        help_text="Nuestros Servicios",
        )
    
    displayNServicios = models.BooleanField(
        "Mostrar",
        default=True,
        help_text="Mostrar Cards de Nuestros Segicios",
        )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("slogan"),
        FieldPanel("imageBG"),
        FieldPanel("imageMain"),
        FieldPanel("imagePromo"),

        MultiFieldPanel([
            FieldPanel("cotizaDescription", classname="full"),
            FieldPanel("mjeCotiza", classname="full"),
            FieldPanel("mjeFueraDeRango", classname="full"),
            FieldPanel("mjeWAContratando", classname="full"),
            FieldPanel("mjeWAFueraDeRango", classname="full"),
        ], heading="Cotiza"),

        MultiFieldPanel([
            FieldPanel("serviviosDescription", classname="full"),
            FieldPanel("displayNServicios"),
            InlinePanel("nuestros_servicios", label="Servicio"),
        ], heading="Nuestros Servicios"),
        
        InlinePanel("preguntas_frecuentes", label="Preguntas Frecuentes"),
    ]


    def save(self, *args, **kwargs):
        print("Se actualizó los valores home")
        cache.clear()
        return super().save(*args, **kwargs)

class nuestrosServicios(Orderable):
    page = ParentalKey(
        HomePage, 
        on_delete=models.CASCADE, 
        related_name='nuestros_servicios'
        )
    image = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.CASCADE,
        blank = True,
        null= True,
        related_name='+'
        )
    titulo = models.CharField(
        blank=False,
        max_length=25
        )
    resumen = models.CharField(
        blank=True,
        null=True,
        max_length=250
        )

    panels = [
        FieldPanel('image'),
        FieldPanel('titulo'),
        FieldPanel('resumen'),
    ]

class preguntasFrecuentes(Orderable):
    page = ParentalKey(
        HomePage, 
        on_delete=models.CASCADE, 
        related_name='preguntas_frecuentes'
        )
# PREGUNTAS FRECUENTES
    pregunta = models.CharField(
        "Pregunta",
        max_length=250,
        blank=True,
        null=True,
        )
    respuesta = models.TextField(
        "Respuesta",
        max_length=500,
        blank=True,
        null=True,
        )

    display = models.BooleanField(
        "Mostrar",
        default=True,
        help_text="Mostrar Pregunta y Respuesta",
        )
    panels = [
        FieldPanel('pregunta'),
        FieldPanel('respuesta'),
        FieldPanel('display'),
    ]


