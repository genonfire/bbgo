from django import template

register = template.Library()


@register.inclusion_tag('boards/like_users.html')
def like_users():
    """Like users"""
    return {}
