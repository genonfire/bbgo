# -*- coding: utf-8 -*-
from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter(name='status_to_text')
def _status_to_text(status):
    if status == '1normal':
        return _('status_published')
    elif status == '2temp':
        return "<font color=#0073aa>%s</font>" % _('status_draft')
    elif status == '3notice':
        return "<b>%s</b>" % _('status_notice')
    elif status == '4warning':
        return "<font color=#FF574F>%s</font>" % _('status_warning')
    elif status == '5hidden':
        return "<font color=#FF574F>%s</font>" % _('status_pending')
    elif status == '6deleted':
        return "<font color=#e54f44>%s</font>" % _('status_deleted')
    elif status == '7spam':
        return "<font color=#FF574F>%s</font>" % _('status_spam')
    elif status == '1proposed':
        return _('status_proposed')
    elif status == '2progress':
        return _('status_progress')
    elif status == '3rejected':
        return "<font color=#e54f44>%s</font>" % _('status_rejected')
    elif status == '4canceled':
        return "<font color=#e54f44>%s</font>" % _('status_canceled')
    elif status == '5completed':
        return "<font color=#0073aa>%s</font>" % _('status_completed')
