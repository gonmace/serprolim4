def project_analytics(request):
    """
    Inyecta la configuración de tracking en todos los templates.
    Uso: {{ project_analytics.gtm }}, {{ project_analytics.fb_pixel }}, etc.
    """
    from .models import TrackingSettings
    try:
        return {'project_analytics': TrackingSettings.get_settings()}
    except Exception:
        from types import SimpleNamespace
        return {'project_analytics': SimpleNamespace(
            gtm='',
            google_analytics='',
            google_ads='',
            adsense='',
            fb_pixel='',
            open_graph='',
            head_scripts='',
            body_scripts='',
        )}
