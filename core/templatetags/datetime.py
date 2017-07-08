from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='is_today')
def _is_today(created_at):
    return timezone.now().date() == created_at.date()
