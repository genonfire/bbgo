from django import template

register = template.Library()


@register.filter(name='range')
def _range(start, stop):
    return range(start, stop)
