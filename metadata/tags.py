from django.template import TemplateSyntaxError
from django.template.loader import render_to_string


def _get_site_name_from_model(request):
    """Get site_name from CountrySettings (admin)."""
    from django.conf import settings
    default = getattr(settings, 'DEFAULT_SITE_NAME', 'MultiSane')
    country = getattr(request, 'country', None)
    if not country:
        from generalData.models import CountrySettings
        country = CountrySettings.objects.filter(country_code='bo').first()
    if country:
        return (country.site_name or default).strip() or default
    return default


def meta_tags(request, model):
    if not request:
        raise TemplateSyntaxError(
            "'meta_tags' missing request from context")
    if not model:
        raise TemplateSyntaxError(
            "'meta_tags' tag is missing a model or object")
    context = {
        'site_name': _get_site_name_from_model(request),
        'twitter_card_type': model.get_twitter_card_type(request),
        'object': model,
    }

    meta_image = model.get_meta_image_url(request)
    if meta_image:
        width, height = model.get_meta_image_dimensions()
        context['meta_image_width'] = width
        context['meta_image_height'] = height
    context['meta_image'] = meta_image

    return render_to_string('tags.html',
                            context, request=request)
