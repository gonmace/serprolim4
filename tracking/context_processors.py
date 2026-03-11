def project_analytics(request):
    """
    Inyecta la configuración de tracking en todos los templates.
    Uso: {{ project_analytics.head_scripts|safe }}, {{ project_analytics.body_scripts|safe }}
    """
    from .models import TrackingSettings
    try:
        return {'project_analytics': TrackingSettings.get_settings()}
    except Exception:
        from types import SimpleNamespace
        return {'project_analytics': SimpleNamespace(head_scripts='', body_scripts='')}
