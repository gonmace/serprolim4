
from django.contrib import admin
from django.urls import path, include

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings

from wfavicon.urls import urls as favicon_urls
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from wagtail.contrib.sitemaps.views import sitemap as wagtail_sitemap_view
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap as WagtailSitemap
from home import views as home_views
from home.sitemaps import HomepageSitemap

def sitemap_view(request, **kwargs):
    """Sitemap que incluye homepage + páginas Wagtail."""
    sitemaps = {
        'home': HomepageSitemap(),
        'wagtail': WagtailSitemap(request),
    }
    return wagtail_sitemap_view(request, sitemaps=sitemaps, **kwargs)

def robots_txt(request):
    """Serve robots.txt with sitemap URL from Wagtail site."""
    template = loader.get_template('robots.txt')
    context = {}
    try:
        from wagtail.models import Site
        site = Site.find_for_request(request)
        if site:
            context['wagtail_site'] = site
        else:
            context['wagtail_site'] = type('Obj', (), {'root_url': 'https://limpiezapozossepticos.com'})()
    except Exception:
        context['wagtail_site'] = type('Obj', (), {'root_url': 'https://limpiezapozossepticos.com'})()
    return HttpResponse(template.render(context), content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_blog/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('sitemap.xml', sitemap_view),
    path('robots.txt', robots_txt),
    path('ads.txt', TemplateView.as_view(
        template_name="ads.txt", content_type='text/plain')
         ),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
    urlpatterns += path("__reload__/", include("django_browser_reload.urls")),


urlpatterns = urlpatterns + [
    path("chat/", include("chat.urls")),
    path("", home_views.landing_view, name='landing'),
    path("", include(favicon_urls)),
    path("", include(wagtail_urls)),
]

# Admin customization: Hide models from standard Django admin
from taggit.models import Tag
from wagtail.documents.models import Document
from wagtail.images.models import Image
from wagtail.models import Collection

def hide_models_from_admin():
    """Unregister models from Django admin if they are registered"""
    models_to_hide = [Tag, Document, Image, Collection]
    
    for model in models_to_hide:
        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass

hide_models_from_admin()
