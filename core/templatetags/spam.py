from django import template
from django.contrib.admin.views.decorators import staff_member_required

from spams.models import IP, Word

register = template.Library()


@staff_member_required
@register.inclusion_tag('spams/show_ips.html', takes_context=True)
def show_ips(context):
    """Show spam IP addresses"""
    ips = IP.objects.all()

    return {
        'ips': ips,
    }


@staff_member_required
@register.inclusion_tag('spams/show_words.html', takes_context=True)
def show_words(context):
    """Show spam words"""
    words = Word.objects.all()

    return {
        'words': words,
    }
