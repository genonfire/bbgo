from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='is_today')
def _is_today(created_at):
    return timezone.localtime(timezone.now()).date() == created_at.date()


@register.filter(name='is_same_date')
def _is_same_day(created_at, modified_at):
    if created_at > modified_at - timezone.timedelta(seconds=1):
        return True
    else:
        return False
