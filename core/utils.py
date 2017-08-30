# -*- coding: utf-8 -*-
"""Utility functions for bbgo"""
from django.shortcuts import render
from django.utils.translation import ugettext as _


def error_page(request, msg=''):
    """Show error page with msg"""
    if not msg:
        msg = _('Wrong access')

    return render(
        request,
        "error.html",
        {
            'msg': msg,
        }
    )


def error_to_response(request, msg=''):
    """Show error response with msg"""
    if not msg:
        msg = _('Wrong access')

    return render(
        request,
        "error_response.html",
        {
            'msg': msg,
        }
    )


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
