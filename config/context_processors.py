from .models import CountrySettings


def site_settings(request):
    """
    Context processor to make CountrySettings available in all templates.
    Usage in templates: {{ site_settings.tel }}, {{ site_settings.email }}, etc.
    """
    if hasattr(request, 'country') and request.country:
        return {'site_settings': request.country}

    default_settings = CountrySettings.objects.filter(country_code='bo').first()
    return {'site_settings': default_settings}
