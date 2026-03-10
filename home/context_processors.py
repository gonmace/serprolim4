"""Context processors for home app."""

def seo_site_name(request):
    """
    Add seo_site_name to context for use in page titles.
    Always uses CountrySettings.site_name from admin (request.country or default 'bo').
    """
    from django.conf import settings
    default = getattr(settings, 'DEFAULT_SITE_NAME', 'MultiSane')

    # 1. CountrySettings from model (request.country or default 'bo')
    country = getattr(request, 'country', None)
    if not country:
        from config.models import CountrySettings
        country = CountrySettings.objects.filter(country_code='bo').first()

    if country:
        return {'seo_site_name': (country.site_name or default).strip() or default}

    # 2. Last resort when no CountrySettings exist yet
    return {'seo_site_name': default}
