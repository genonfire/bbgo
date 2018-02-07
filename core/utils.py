# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext as _


def error_page(request, errormsg=''):
    """Show error page with message"""
    if not errormsg:
        errormsg = _('Wrong access')

    return render(
        request,
        "error.html",
        {
            'errormsg': errormsg,
        }
    )


def error_to_response(request, errormsg=''):
    """Show error response with msg"""
    if not errormsg:
        errormsg = _('Wrong access')

    return render(
        request,
        "error_response.html",
        {
            'errormsg': errormsg,
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


def get_referrer(request):
    """Return referrer"""
    referrer = request.META['HTTP_REFERER']
    return referrer


def get_useragent(request):
    """Return useragent"""
    user_agent = request.META['HTTP_USER_AGENT']
    return user_agent


def is_mobile(request):
    """Return true if request from Android and iPhone"""
    user_agent = request.META['HTTP_USER_AGENT']
    if 'Android' in user_agent or 'iPhone' in user_agent:
        return True
    else:
        return False


def get_referer(request):
    """Get referer URL to stay"""
    referer = request.META.get('HTTP_REFERER')
    return referer
