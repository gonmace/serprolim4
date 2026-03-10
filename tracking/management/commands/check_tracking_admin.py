"""Comando: py manage.py check_tracking_admin"""
from django.core.management.base import BaseCommand
from tracking.models import TrackingSettings
from tracking.admin import TrackingSettingsAdmin, TrackingSettingsForm
from django.contrib import admin
from django.test import RequestFactory


class Command(BaseCommand):
    help = "Verifica qué campos tiene el form del admin de Tracking"

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write("No hay superuser.")
            return
        request = RequestFactory().get('/admin/')
        request.user = user

        obj = TrackingSettings.get_settings()

        form = TrackingSettingsForm(instance=obj)
        self.stdout.write(f"TrackingSettingsForm campos: {[f.name for f in form.visible_fields()]}")
        self.stdout.write(f"Total: {len(form.visible_fields())}")

        admin_obj = TrackingSettingsAdmin(TrackingSettings, admin.site)
        admin_form_class = admin_obj.get_form(request, obj=obj)
        form2 = admin_form_class(instance=obj)
        self.stdout.write(f"Admin form campos: {[f.name for f in form2.visible_fields()]}")
