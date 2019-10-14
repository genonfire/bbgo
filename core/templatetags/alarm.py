from django import template

register = template.Library()


@register.inclusion_tag('accounts/alarm_list.html')
def alarm_list():
    """Alarm list"""
    return {}
