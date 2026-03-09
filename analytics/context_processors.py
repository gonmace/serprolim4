"""Context processors for analytics app (antes wanalytics)."""

def project_analytics(request):
    """
    Analytics a nivel proyecto.
    Uso en templates: {{ project_analytics.gtm_id }}, {{ project_analytics.gads_id }}, etc.
    """
    from .models import AnalyticsSettings
    try:
        settings = AnalyticsSettings.get_settings()
        return {'project_analytics': settings}
    except Exception:
        from types import SimpleNamespace
        return {'project_analytics': SimpleNamespace(
            gtm_id='', gads_id='', ga_g_tracking_id='', head_scripts='', body_scripts=''
        )}
