from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        """Unregister Wagtail models from Django Admin after all apps are loaded."""
        from django.contrib import admin
        from taggit.models import Tag
        from wagtail.documents.models import Document
        from wagtail.images.models import Image

        try:
            admin.site.unregister(Tag)
            admin.site.unregister(Document)
            admin.site.unregister(Image)
        except admin.sites.NotRegistered:
            pass

