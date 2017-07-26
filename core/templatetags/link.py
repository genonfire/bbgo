from django import template

register = template.Library()


@register.filter(name='target_blank', is_safe=True)
def _target_blank(link):
    return link.replace('<a href=', '<a target="_blank" href=')
