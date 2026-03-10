from django.utils.safestring import mark_safe
from django import template
import re

register = template.Library()


@register.filter(name='titulo')
def titulo(text):
    titulo = re.sub('\s\s', '<br>', text)
    return mark_safe(titulo)
