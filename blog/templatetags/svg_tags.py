"""
Template tag to inject SVG content inline so it can inherit CSS (e.g. currentColor).
Usage: {% load svg_tags %} ... {% inline_svg 'img/multisane.svg' class='h-12 w-auto' %}
"""
import re
from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def inline_svg(path, class_name="", color_var=""):
    """
    Read an SVG file from static files and inject it inline.
    This allows the SVG to inherit color via currentColor from the parent.
    :param path: Static file path (e.g. 'img/multisane.svg')
    :param class_name: Optional CSS classes for the root svg element
    :param color_var: Optional CSS variable for color (e.g. 'primary-content' for var(--color-primary-content))
    """
    full_path = find(path)
    if not full_path:
        return ""
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, IOError):
        return ""

    # Strip XML declaration and comments for cleaner HTML
    content = re.sub(r'<\?xml[^>]*\?>', '', content)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = content.strip()

    attrs = []
    if class_name:
        attrs.append(f'class="{class_name.replace(chr(34), "")}"')
    if color_var:
        attrs.append(f'style="color: var(--color-{color_var})"')

    if attrs:
        attrs_str = " " + " ".join(attrs)
        def add_attrs(match):
            return f'<svg{match.group(1)}{attrs_str}'
        content = re.sub(r'<svg(\s[^>]*)', add_attrs, content, count=1)
        if '<svg ' not in content[:10]:
            content = content.replace('<svg>', f'<svg{attrs_str}>', 1)

    return mark_safe(content)


@register.simple_tag
def inline_svg_image(image, class_name="", color_var=""):
    """
    Render a Wagtail image inline if it's an SVG, otherwise return empty string.
    Usage: {% inline_svg_image site_settings.icon class_name='h-10 w-auto' as logo %}
            {% if logo %}{{ logo }}{% else %}<img src="{{ site_settings.icon.url }}">{% endif %}
    """
    if not image:
        return ""
    try:
        file_name = image.file.name.lower()
        if not file_name.endswith(".svg"):
            return ""
        with open(image.file.path, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, IOError, AttributeError, ValueError):
        return ""

    content = re.sub(r'<\?xml[^>]*\?>', '', content)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = content.strip()

    attrs = ['fill="currentColor"']
    if class_name:
        attrs.append(f'class="{class_name.replace(chr(34), "")}"')
    if color_var:
        attrs.append(f'style="color: var(--color-{color_var})"')

    attrs_str = " " + " ".join(attrs)

    def add_attrs(match):
        return f'<svg{match.group(1)}{attrs_str}'

    content = re.sub(r'<svg(\s[^>]*)', add_attrs, content, count=1)
    if not content.lstrip().startswith('<svg '):
        content = content.replace('<svg>', f'<svg{attrs_str}>', 1)

    return mark_safe(content)
