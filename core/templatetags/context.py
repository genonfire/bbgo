from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def request_path(context):
    """Return request.path"""
    return context['request'].path
