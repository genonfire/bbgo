# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('accounts/show_terms.html')
def show_terms():
    """Show Terms of service and Privacy Policy"""
    return {
        "SITE_NAME": settings.SITE_NAME
    }
