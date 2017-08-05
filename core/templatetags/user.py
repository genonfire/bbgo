from django import template

register = template.Library()


@register.filter(name='nickname')
def _nickname(user):
    if user.first_name:
        return user.first_name
    return user
