from django import template

from base import metatags

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context, model=None):
    request = context.get('request', None)
    if not model:
        model = context.get('self', None)
    return metatags.meta_tags(request, model)
