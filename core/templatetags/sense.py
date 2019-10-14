from django import template
from django.conf import settings
from django.urls import resolve

register = template.Library()


@register.inclusion_tag('show_sense.html', takes_context=True)
def show_up_sense(context, sense=''):
    """Show AdSense for SENSE_UP"""
    request = context['request']
    if sense == 'user':
        user = request.user
        if user.profile.sense_client and user.profile.sense_slot:
            sense_client = user.profile.sense_client
            sense_slot = user.profile.sense_slot
        else:
            sense_client = settings.SENSE_UP_CLIENT
            sense_slot = settings.SENSE_UP_SLOT
    else:
        sense_client = settings.SENSE_UP_CLIENT
        sense_slot = settings.SENSE_UP_SLOT

    sense_enabled = settings.ENABLE_ADSENSE
    if settings.DEBUG:
        sense_enabled = False

    return {
        'sense_enabled': sense_enabled,
        'sense_native': False,
        'sense_client': sense_client,
        'sense_slot': sense_slot,
    }


@register.inclusion_tag('show_sense.html', takes_context=True)
def show_up_sense_native(context, sense=''):
    """Show AdSense Native for SENSE_UP"""
    request = context['request']
    if sense == 'user':
        user = request.user
        if user.profile.sense_client and user.profile.sense_slot:
            sense_client = user.profile.sense_client
            sense_slot = user.profile.sense_slot
        else:
            sense_client = settings.SENSE_UP_CLIENT
            sense_slot = settings.SENSE_UP_SLOT
    else:
        sense_client = settings.SENSE_UP_CLIENT
        sense_slot = settings.SENSE_UP_SLOT

    sense_enabled = settings.ENABLE_ADSENSE
    if settings.DEBUG:
        sense_enabled = False

    return {
        'sense_enabled': sense_enabled,
        'sense_native': True,
        'sense_client': sense_client,
        'sense_slot': sense_slot,
    }


@register.inclusion_tag('show_sense.html', takes_context=True)
def show_down_sense(context, sense=''):
    """Show AdSense for SENSE_DOWN"""
    request = context['request']
    if sense == 'user':
        user = request.user
        if user.profile.sense_client and user.profile.sense_slot:
            sense_client = user.profile.sense_client
            sense_slot = user.profile.sense_slot
        else:
            sense_client = settings.SENSE_DOWN_CLIENT
            sense_slot = settings.SENSE_DOWN_SLOT
    else:
        sense_client = settings.SENSE_DOWN_CLIENT
        sense_slot = settings.SENSE_DOWN_SLOT

    sense_enabled = settings.ENABLE_ADSENSE
    if settings.DEBUG:
        sense_enabled = False

    return {
        'sense_enabled': sense_enabled,
        'sense_native': False,
        'sense_client': sense_client,
        'sense_slot': sense_slot,
    }


@register.inclusion_tag('show_sense.html', takes_context=True)
def show_down_sense_native(context, sense=''):
    """Show AdSense Native for SENSE_DOWN"""
    request = context['request']
    if sense == 'user':
        user = request.user
        if user.profile.sense_client and user.profile.sense_slot:
            sense_client = user.profile.sense_client
            sense_slot = user.profile.sense_slot
        else:
            sense_client = settings.SENSE_DOWN_CLIENT
            sense_slot = settings.SENSE_DOWN_SLOT
    else:
        sense_client = settings.SENSE_DOWN_CLIENT
        sense_slot = settings.SENSE_DOWN_SLOT

    sense_enabled = settings.ENABLE_ADSENSE
    if settings.DEBUG:
        sense_enabled = False

    return {
        'sense_enabled': sense_enabled,
        'sense_native': True,
        'sense_client': sense_client,
        'sense_slot': sense_slot,
    }


@register.inclusion_tag('show_sense.html', takes_context=True)
def show_side_sense(context, sense=''):
    """Show AdSense for SENSE_SIDE"""
    request = context['request']
    if sense == 'user':
        user = request.user
        if user.profile.sense_client and user.profile.sense_slot:
            sense_client = user.profile.sense_client
            sense_slot = user.profile.sense_slot
        else:
            sense_client = settings.SENSE_SIDE_CLIENT
            sense_slot = settings.SENSE_SIDE_SLOT
    else:
        sense_client = settings.SENSE_SIDE_CLIENT
        sense_slot = settings.SENSE_SIDE_SLOT

    sense_enabled = settings.ENABLE_ADSENSE
    if settings.DEBUG:
        sense_enabled = False
    else:
        app = resolve(request.path).namespace
        if app == 'vaults':
            sense_enabled = False

    return {
        'sense_enabled': sense_enabled,
        'sense_native': False,
        'sense_client': sense_client,
        'sense_slot': sense_slot,
    }


@register.inclusion_tag('show_sense.html', takes_context=True)
def show_side_sense_native(context, sense=''):
    """Show AdSense Native for SENSE_SIDE"""
    request = context['request']
    if sense == 'user':
        user = request.user
        if user.profile.sense_client and user.profile.sense_slot:
            sense_client = user.profile.sense_client
            sense_slot = user.profile.sense_slot
        else:
            sense_client = settings.SENSE_SIDE_CLIENT
            sense_slot = settings.SENSE_SIDE_SLOT
    else:
        sense_client = settings.SENSE_SIDE_CLIENT
        sense_slot = settings.SENSE_SIDE_SLOT

    sense_enabled = settings.ENABLE_ADSENSE
    if settings.DEBUG:
        sense_enabled = False
    else:
        app = resolve(request.path).namespace
        if app == 'vaults':
            sense_enabled = False

    return {
        'sense_enabled': sense_enabled,
        'sense_native': True,
        'sense_client': sense_client,
        'sense_slot': sense_slot,
    }
