
from django.contrib import admin
from django.urls import path, include

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings

from wfavicon.urls import urls as favicon_urls
from django.views.generic import TemplateView
from wagtail.contrib.sitemaps.views import sitemap
from home import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_blog/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('sitemap.xml', sitemap),
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
    path("", home_views.landing_view, name='landing'),
    path("", include(favicon_urls)),
    path("", include(wagtail_urls)),
]
