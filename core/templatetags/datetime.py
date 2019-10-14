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


@register.filter(name='is_recent')
def _is_recent(created_at):
    recent = timezone.localtime(timezone.now()) - timezone.timedelta(hours=1)
    if recent < created_at:
        return True
    else:
        return False


@register.filter(name='is_lately')
def _is_lately(created_at):
    lately = timezone.localtime(timezone.now()) - timezone.timedelta(days=1)
    if lately < created_at:
        return True
    else:
        return False
