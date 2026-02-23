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

# --- NEW DJANGO MODELS ---
from wgeneralData.models import CountrySettings

class LandingPage(models.Model):
    country = models.ForeignKey(
        CountrySettings,
        on_delete=models.CASCADE,
        related_name='landing_pages',
        verbose_name="Country Config",
        null=True, 
        blank=True
    )
    enabled = models.BooleanField(
        default=False, 
        verbose_name="Enabled",
        help_text="Check to make this the active Landing Page for the selected country."
    )

    seo_title = models.CharField(
        "SEO Title",
        max_length=70,
        blank=True,
        null=True,
        default="Limpieza de pozos y cámaras sépticas",
        help_text="Título para buscadores y redes sociales (ej: Limpieza de pozos y cámaras sépticas)",
    )
    search_description = models.TextField(
        "Meta Description",
        max_length=160,
        blank=True,
        null=True,
        default="SerProLim - Limpieza de pozos ciegos y cámaras sépticas en Santa Cruz. Cotiza en línea. Puntualidad y buen servicio.",
        help_text="Descripción para buscadores (máx 160 caracteres)",
    )

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
    # Using Wagtail Images still as they are just database references to files
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

    class Meta:
        verbose_name = "Landing Page"
        verbose_name_plural = "Landing Page"

    def __str__(self):
        return f"Landing Page - {self.country.name if self.country else 'No Country'} ({'Enabled' if self.enabled else 'Disabled'})"
    
    def save(self, *args, **kwargs):
        if self.enabled and self.country:
            # Disable all other pages for this country
            LandingPage.objects.filter(country=self.country).exclude(pk=self.pk).update(enabled=False)
        cache.clear()
        super().save(*args, **kwargs)

    @property
    def title(self):
        """Alias for templates expecting Page-like title (base.html)."""
        return self.seo_title or self.subtitle or "Limpieza de pozos y cámaras sépticas"

    @property
    def canonical_url(self):
        """Return None - LandingPage uses request path for canonical (handled by base)."""
        return None

class LandingService(models.Model):
    landing_page = models.ForeignKey(
        LandingPage,
        related_name='nuestros_servicios',
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        'wagtailimages.Image', 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
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
    
    # For ordering if needed, but simple FK is start
    sort_order = models.IntegerField(null=True, blank=True, editable=False)
    
    class Meta:
         ordering = ['sort_order']

    def __str__(self):
        return self.titulo

class LandingFAQ(models.Model):
    landing_page = models.ForeignKey(
        LandingPage,
        related_name='preguntas_frecuentes',
        on_delete=models.CASCADE,
    )
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
    
    sort_order = models.IntegerField(null=True, blank=True, editable=False)
    
    class Meta:
         ordering = ['sort_order']

    def __str__(self):
        return self.pregunta or "Pregunta"


# --- EXISTING WAGTAIL MODELS (Deprecated) ---

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
