"""
Configura un Site de Wagtail para desarrollo local (localhost).
Así los enlaces a posts no redirigen a producción.

Ejecutar en desarrollo:
    python manage.py setup_localhost_site

O con puerto personalizado:
    python manage.py setup_localhost_site --port 8000
"""
from django.core.management.base import BaseCommand
from wagtail.models import Site


class Command(BaseCommand):
    help = "Añade o actualiza un Site de Wagtail para localhost (evita redirección a producción)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Puerto para localhost (default: 8000)',
        )
        parser.add_argument(
            '--hostname',
            default='localhost',
            help='Hostname (default: localhost)',
        )

    def handle(self, *args, **options):
        hostname = options['hostname']
        port = options['port']

        # Obtener el root_page del sitio existente
        try:
            existing_site = Site.objects.get(is_default_site=True)
        except Site.DoesNotExist:
            existing_site = Site.objects.first()

        if not existing_site:
            self.stdout.write(self.style.ERROR('No hay Sites configurados. Crea uno en Wagtail Admin → Settings → Sites primero.'))
            return

        root_page = existing_site.root_page
        localhost_site = Site.objects.filter(hostname=hostname, port=port).first()

        if localhost_site:
            localhost_site.root_page = root_page
            localhost_site.save()
            self.stdout.write(self.style.SUCCESS(f'Site actualizado: {hostname}:{port}'))
        else:
            Site.objects.create(
                hostname=hostname,
                port=port,
                root_page=root_page,
                is_default_site=False,
                site_name=f'Local ({hostname}:{port})',
            )
            self.stdout.write(self.style.SUCCESS(f'Site creado: {hostname}:{port}'))

        self.stdout.write('Los enlaces a posts deberían funcionar en localhost.')
