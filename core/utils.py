# -*- coding: utf-8 -*-
"""Utility functions for bbgo"""


def get_ipaddress(request):
    """Return ipaddress"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_mobile(request):
    """Return true if request from Android and iPhone"""
    user_agent = request.META['HTTP_USER_AGENT']
    if 'Android' in user_agent or 'iPhone' in user_agent:
        return True
    else:
        return False


def get_template(request, template):
    """Return template name according to UA"""
    if is_mobile(request):
        return template.replace('m-', '')
    else:
        return template.replace('m-', '')
