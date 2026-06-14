"""
Script para agregar la sección de precios al artículo estrella.
Ejecutar en el VPS con:
    docker compose exec serprolim5 python manage.py shell < add_precio.py
"""
import json
import uuid
from django.db import connection
from blog.models import BlogPage

# ─────────────────────────────────────────────
# 1. Buscar la página
# ─────────────────────────────────────────────
try:
    page = BlogPage.objects.get(slug='pozo-ciego-se-llena-muy-rapido')
except BlogPage.DoesNotExist:
    print("ERROR: No se encontró la página con slug 'pozo-ciego-se-llena-muy-rapido'")
    exit(1)

print(f"Página encontrada: {page.title}  (ID: {page.pk})")

# ─────────────────────────────────────────────
# 2. Leer el JSON del campo body desde la base de datos
# ─────────────────────────────────────────────
cursor = connection.cursor()
cursor.execute("SELECT body FROM blog_blogpage WHERE page_ptr_id = %s", [page.pk])
row = cursor.fetchone()

if row is None or row[0] is None:
    print("ERROR: El campo body está vacío.")
    exit(1)

body_json = json.loads(row[0]) if isinstance(row[0], str) else row[0]
print(f"Bloques actuales: {len(body_json)}")

# Mostrar encabezados para verificación
print("\nEncabezados en el artículo:")
for i, block in enumerate(body_json):
    if block.get('type') == 'heading_block':
        print(f"  [{i}] {block['value'].get('heading_text', '')}")

# ─────────────────────────────────────────────
# 3. Encontrar la posición de "Conclusión"
# ─────────────────────────────────────────────
conclusion_idx = None
for i, block in enumerate(body_json):
    if block.get('type') == 'heading_block':
        heading_text = block['value'].get('heading_text', '')
        if 'Conclusi' in heading_text:
            conclusion_idx = i
            print(f"\n-> Se insertará ANTES del índice {i}: '{heading_text}'")
            break

if conclusion_idx is None:
    # Si no hay "Conclusión", agregar al final
    conclusion_idx = len(body_json)
    print(f"\nNo se encontró 'Conclusión'. Los bloques se agregarán al final (índice {conclusion_idx}).")

# ─────────────────────────────────────────────
# 4. Construir los nuevos bloques
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# 5. Insertar antes de "Conclusión"
# ─────────────────────────────────────────────
body_json.insert(conclusion_idx, new_paragraph)
body_json.insert(conclusion_idx, new_heading)

print(f"\n2 bloques insertados en posición {conclusion_idx}.")
print(f"Total de bloques: {len(body_json)}")

# ─────────────────────────────────────────────
# 6. Guardar con revisión y publicar
# ─────────────────────────────────────────────
page.body = body_json        # StreamField acepta lista de dicts con use_json_field=True
revision = page.save_revision()
revision.publish()

print("\n✓ Sección de precios agregada y página publicada exitosamente.")
print(f"  URL: https://limpiezapozossepticos.com{page.url_path.replace('/root', '')}")
