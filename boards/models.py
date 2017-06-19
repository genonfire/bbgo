# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models


class Board(models.Model):
    """Board of boards"""

    table = models.CharField(max_length="31", choices=settings.BOARD_TABLES, default='0')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True)
    ip = models.GenericIPAddressField()
    category = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    like_users = models.TextField(default='', blank=True)
    dislike_users = models.TextField(default='', blank=True)
    replies = models.TextField(default='', blank=True)

    def get_absolute_url(self):
        """Back to list"""
        return reverse_lazy('board show list', args=[self.table])
