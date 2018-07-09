# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
# from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Attachment(models.Model):
    """Attachment of papers"""

    file = models.FileField(upload_to="paper-files/%Y-%m-%d/")
    content_type = models.CharField(max_length=255, default='')


class Support(models.Model):
    """Support of papers"""

    order = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024, default='', blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    approved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta for ordering"""

        ordering = ['order']


class Person(models.Model):
    """Person of papers"""

    order = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        """Meta for ordering"""

        ordering = ['order']


class Paper(models.Model):
    """Paper of papers"""

    PAPER_STATUS = {
        ('1proposed', _('status_proposed')),
        ('2progress', _('status_progress')),
        ('3rejected', _('status_rejected')),
        ('4canceled', _('status_canceled')),
        ('5completed', _('status_completed')),
    }

    status = models.CharField(
        max_length=12, choices=PAPER_STATUS, default='1proposed')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=41)
    content = models.TextField()
    files = models.ManyToManyField(Attachment, blank=True)
    cc = models.ManyToManyField(
        Person, related_name='paper_cc', default='', blank=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paper_approver")
    comment = models.CharField(
        max_length=settings.APPROVE_COMMENT_MAX, default='', blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    approved_at = models.DateTimeField(auto_now_add=True)
    supporters = models.ManyToManyField(
        Support, related_name='paper_supporters', blank=True)
    cancelmsg = models.CharField(
        max_length=settings.APPROVE_COMMENT_MAX, default='', blank=True)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    notifiers = models.ManyToManyField(
        Person, related_name='paper_notifiers', default='', blank=True)
