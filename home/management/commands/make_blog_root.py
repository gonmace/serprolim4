"""
Comando para hacer que BlogIndexPage sea la raíz de Wagtail, eliminando HomePage.

Ejecutar una sola vez después de migrar:
    python manage.py make_blog_root

Mueve BlogIndexPage al nivel raíz, actualiza Site.root_page y elimina HomePage.
Las StandardPage que estaban bajo Home se mueven también a la raíz.
"""
from django.core.management.base import BaseCommand
from wagtail.models import Site, Page


class Command(BaseCommand):
    help = "Mueve BlogIndexPage a la raíz de Wagtail y elimina HomePage"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se haría sin ejecutar cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('Modo dry-run: no se harán cambios'))

        try:
            site = Site.objects.get(is_default_site=True)
        except Site.DoesNotExist:
            site = Site.objects.first()
        if not site:
            self.stdout.write(self.style.ERROR('No se encontró ningún Site de Wagtail'))
            return

        home = site.root_page.specific
        if home.__class__.__name__ != 'HomePage':
            self.stdout.write(
                self.style.SUCCESS(f'Ya está configurado: root_page es {home.__class__.__name__}')
            )
            return

        root_page = Page.objects.get(depth=1)
        children = list(home.get_children().specific())

        blog_index = None
        others = []
        for child in children:
            if child.__class__.__name__ == 'BlogIndexPage':
                blog_index = child
            else:
                others.append(child)

        if not blog_index:
            self.stdout.write(self.style.ERROR('No se encontró BlogIndexPage bajo HomePage'))
            return

        if dry_run:
            self.stdout.write(f'Se movería BlogIndexPage (id={blog_index.id}) a la raíz')
            for o in others:
                self.stdout.write(f'  - {o.__class__.__name__} (id={o.id}) a la raíz')
            self.stdout.write(f'  - Site.root_page -> BlogIndexPage')
            self.stdout.write(f'  - Eliminar HomePage (id={home.id})')
            return

        # Mover BlogIndexPage primero (como primer hijo de root)
        blog_index.move(root_page, pos='first-child')
        self.stdout.write(f'Movido BlogIndexPage a la raíz')

        # Mover el resto de hijos
        for child in others:
            try:
                child.move(root_page, pos='last-child')
                self.stdout.write(f'Movido {child.__class__.__name__} (id={child.id}) a la raíz')
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'No se pudo mover {child}: {e}')
                )

        # Actualizar Site
        site.root_page = blog_index
        site.save()
        self.stdout.write('Site.root_page actualizado a BlogIndexPage')

        # Eliminar HomePage
        home.delete()
        self.stdout.write(self.style.SUCCESS('HomePage eliminada. Wagtail solo tiene Blog como raíz.'))
