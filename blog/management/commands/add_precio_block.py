import json
import uuid
from django.core.management.base import BaseCommand
from django.db import connection
from blog.models import BlogPage


class Command(BaseCommand):
    help = 'Agrega la sección de precios al artículo estrella del pozo ciego'

    def handle(self, *args, **options):
        try:
            page = BlogPage.objects.get(slug='pozo-ciego-se-llena-muy-rapido')
        except BlogPage.DoesNotExist:
            self.stderr.write("ERROR: No se encontró la página con slug 'pozo-ciego-se-llena-muy-rapido'")
            return

        self.stdout.write(f"Página encontrada: {page.title}  (ID: {page.pk})")

        cursor = connection.cursor()
        cursor.execute("SELECT body FROM blog_blogpage WHERE page_ptr_id = %s", [page.pk])
        row = cursor.fetchone()

        if row is None or row[0] is None:
            self.stderr.write("ERROR: El campo body está vacío.")
            return

        body_json = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        self.stdout.write(f"Bloques actuales: {len(body_json)}")

        # Verificar si la sección ya existe
        for block in body_json:
            if block.get('type') == 'heading_block':
                if 'cuesta vaciar' in block['value'].get('heading_text', '').lower():
                    self.stdout.write(self.style.WARNING("La sección de precios ya existe. No se hicieron cambios."))
                    return

        # Mostrar encabezados
        self.stdout.write("\nEncabezados en el artículo:")
        for i, block in enumerate(body_json):
            if block.get('type') == 'heading_block':
                self.stdout.write(f"  [{i}] {block['value'].get('heading_text', '')}")

        # Encontrar posición de "Conclusión"
        conclusion_idx = None
        for i, block in enumerate(body_json):
            if block.get('type') == 'heading_block':
                if 'Conclusi' in block['value'].get('heading_text', ''):
                    conclusion_idx = i
                    break

        if conclusion_idx is None:
            conclusion_idx = len(body_json)
            self.stdout.write(f"\nNo se encontró 'Conclusión'. Se agrega al final (índice {conclusion_idx}).")
        else:
            self.stdout.write(f"\nInsertar antes del índice {conclusion_idx}.")

        new_heading = {
            "type": "heading_block",
            "value": {
                "heading_text": "¿Cuánto cuesta vaciar un pozo ciego?",
                "size": "h2"
            },
            "id": str(uuid.uuid4())
        }

        new_paragraph = {
            "type": "paragraph_block",
            "value": (
                "<p>El factor que más influye en el precio es la <b>distancia entre tu domicilio y la planta de tratamiento de aguas</b>. "
                "El camión atmosférico debe trasladar los residuos hasta allí, y a mayor distancia, mayor el costo del viaje. "
                "Por eso, el precio puede variar significativamente entre distintas localidades o zonas.</p>"
                "<p>Otros factores que también afectan el valor final:</p>"
                "<ul>"
                "<li><b>Volumen acumulado:</b> a mayor cantidad de residuos, mayor el trabajo de vaciado.</li>"
                "<li><b>Accesibilidad del lugar:</b> zonas de difícil ingreso para el camión pueden tener un recargo adicional.</li>"
                "</ul>"
                "<p>Para conocer el precio exacto en tu zona, lo más conveniente es solicitar una cotización directamente con el proveedor local.</p>"
            ),
            "id": str(uuid.uuid4())
        }

        body_json.insert(conclusion_idx, new_paragraph)
        body_json.insert(conclusion_idx, new_heading)

        page.body = body_json
        revision = page.save_revision()
        revision.publish()

        self.stdout.write(self.style.SUCCESS("\n✓ Sección de precios agregada y página publicada exitosamente."))
