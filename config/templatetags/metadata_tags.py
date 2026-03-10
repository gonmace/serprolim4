from django import template

from config.metadata import meta_tags as render_meta_tags

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_tags(context, model=None):
    request = context.get('request', None)
    if not model:
        model = context.get('self', None)
    return render_meta_tags(request, model)
