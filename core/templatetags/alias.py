# -*- coding: utf-8 -*-
from aliases.models import Alias

from django import template
from django.contrib.auth.decorators import login_required


register = template.Library()


@login_required
@register.inclusion_tag('aliases/show_aliases.html', takes_context=True)
def show_aliases(context):
    """Show aliases"""
    user = context['request'].user
    aliases = Alias.objects.filter(user=user).all()

    return {
        'aliases': aliases,
    }
