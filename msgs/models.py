# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _


class Msg(models.Model):
    """Message of msgs"""

    MSG_STATUS = {
        ('1normal', _('status_normal')),
        ('2read', _('status_read')),
        ('5hidden', _('status_hidden')),
        ('6deleted', _('status_deleted')),
    }

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='msg_sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='msg_recipient', on_delete=models.CASCADE)
    sender_status = models.CharField(
        max_length=10, choices=MSG_STATUS, default='1normal')
    recipient_status = models.CharField(
        max_length=10, choices=MSG_STATUS, default='1normal')
    text = models.TextField(max_length=settings.MSG_TEXT_MAX)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()

    def get_absolute_url(self):
        """Back to list"""
        return reverse_lazy('msgs:inbox', kwargs={'page': 1})
