"""
SEO metadata mixins and meta_tags for Open Graph / Twitter Cards.
Wagtail pages have seo_title, search_description built-in; we add search_image and rendering.
"""
from django.conf import settings
from django.db import models
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy

from wagtail.admin.panels import FieldPanel, MultiFieldPanel


def get_image_model_string():
    try:
        return settings.WAGTAILIMAGES_IMAGE_MODEL
    except AttributeError:
        return 'wagtailimages.Image'


class MetadataMixin(object):
    """An object that can be shared on social media."""

    def get_meta_url(self):
        raise NotImplementedError()

    def get_meta_title(self):
        raise NotImplementedError()

    def get_object_title(self):
        return self.get_meta_title()

    def get_meta_description(self):
        raise NotImplementedError()

    def get_meta_image_url(self, request):
        return None

    def get_meta_image_dimensions(self):
        return None, None

    def get_twitter_card_type(self, request):
        if self.get_meta_image_url(request) is not None:
            return 'summary_large_image'
        return 'summary'


class WagtailImageMetadataMixin(MetadataMixin):
    """Uses a Wagtail Image for image-based metadata."""

    def get_meta_image(self):
        raise NotImplementedError()

    def get_meta_image_rendition(self):
        meta_image = self.get_meta_image()
        if meta_image:
            filter_name = getattr(settings, "WAGTAILMETADATA_IMAGE_FILTER", "fill-1200x630")
            return meta_image.get_rendition(filter=filter_name)
        return None

    def get_meta_image_url(self, request):
        rendition = self.get_meta_image_rendition()
        if rendition:
            return request.build_absolute_uri(rendition.url)
        return None

    def get_meta_image_dimensions(self):
        rendition = self.get_meta_image_rendition()
        if rendition:
            return rendition.width, rendition.height
        return None, None


class MetadataPageMixin(WagtailImageMetadataMixin, models.Model):
    """Mixin for Wagtail pages: adds search_image and promote_panels for SEO."""
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=gettext_lazy('Search image')
    )

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('search_image'),
            FieldPanel('show_in_menus'),
        ], gettext_lazy('Common page configuration')),
    ]

    def get_meta_url(self):
        return self.full_url

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_image(self):
        return self.search_image

    class Meta:
        abstract = True


# --- meta_tags for templates ---
def _get_site_name(request):
    default = getattr(settings, 'DEFAULT_SITE_NAME', 'MultiSane')
    country = getattr(request, 'country', None)
    if not country:
        from config.models import CountrySettings
        country = CountrySettings.objects.filter(country_code='bo').first()
    if country:
        return (country.site_name or default).strip() or default
    return default


def meta_tags(request, model, og_type='website'):
    """Render Open Graph and Twitter Card meta tags."""
    if not request or not model:
        return ''
    context = {
        'site_name': _get_site_name(request),
        'twitter_card_type': model.get_twitter_card_type(request),
        'og_type': og_type,
        'object': model,
    }
    meta_image = model.get_meta_image_url(request)
    if meta_image:
        width, height = model.get_meta_image_dimensions()
        context['meta_image_width'] = width
        context['meta_image_height'] = height
    context['meta_image'] = meta_image
    return render_to_string('tags.html', context, request=request)
