from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='nickname')
def _nickname(user):
    if settings.ENABLE_NICKNAME and user.first_name:
        return user.first_name
    return user
