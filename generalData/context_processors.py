from .models import GeneralSettings, CountrySettings


def site_settings(request):
    """
    Context processor to make GeneralSettings available in all templates
    Usage in templates: {{ site_settings.tel }}, {{ site_settings.email }}, etc.
    """
    # If CountryMiddleware has identified a country, use its settings
    if hasattr(request, 'country') and request.country:
        return {
            'site_settings': request.country
        }

    # Fallback to default CountrySettings (e.g., 'bo' - Bolivia)
    default_settings = CountrySettings.objects.filter(country_code='bo').first()
    
    # If no default exists yet (e.g. before migration), we might return None or handle gracefully
    # But theoretically migration should have created it.
    
    return {
        'site_settings': default_settings
    }
