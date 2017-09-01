# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext as _


class Team(models.Model):
    """Team of teams"""

    TEAM_STATUS = {
        ('1normal', _('status_normal')),
        ('5hidden', _('status_hidden')),
        ('6deleted', _('status_deleted')),
        ('7canceled', _('status_canceled')),
        ('8full', _('status_full')),
    }

    table = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10, choices=TEAM_STATUS, default='1normal')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    category = models.CharField(max_length=23, blank=True)
    subject = models.CharField(max_length=41)
    content = models.TextField(default='', blank=True)
    view_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    slot = models.IntegerField(default=1)
    slot_total = models.IntegerField(default=6)
    slot_users = models.TextField(default='', blank=True)
    # slot_users = models.ManyToManyField(User)

    def get_absolute_url(self):
        """Back to list"""
        return reverse_lazy('teams:recruitment', args=[self.table, 1])

    def get_article_url(self):
        """Back to article"""
        return reverse_lazy('teams:show_recruitment', args=[self.id])

    def get_status_text(self):
        """Get status text"""
        if self.status == '1normal':
            return _('status_normal')
        elif self.status == '5hidden':
            return _('status_hidden')
        elif self.status == '6deleted':
            return _('status_deleted')
        elif self.status == '7canceled':
            return _('status_canceled')
        elif self.status == '8full':
            return _('status_full')


class TeamReply(models.Model):
    """Reply of teams"""

    REPLY_STATUS = {
        ('1normal', _('status_normal')),
        ('5hidden', _('status_hidden')),
        ('6deleted', _('status_deleted')),
    }

    article_id = models.IntegerField(default=0)
    reply_id = models.IntegerField(default=0)
    reply_to = models.CharField(max_length=150, default='', blank=True)
    status = models.CharField(
        max_length=10, choices=REPLY_STATUS, default='1normal')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    content = models.TextField(max_length=settings.REPLY_TEXT_MAX)
