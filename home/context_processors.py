"""Context processors for home app."""

def seo_site_name(request):
    """
    Add seo_site_name to context for use in page titles.
    Uses Wagtail Site when available, otherwise defaults to 'serprolim'.
    """
    try:
        from wagtail.models import Site
        site = Site.find_for_request(request)
        if site:
            return {'seo_site_name': site.site_name}
    except Exception:
        pass
    return {'seo_site_name': 'serprolim'}
