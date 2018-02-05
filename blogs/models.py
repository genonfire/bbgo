# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext as _


class Blog(models.Model):
    """Blog of blogs"""

    BLOG_STATUS = {
        ('1normal', _('status_published')),
        ('2temp', _('status_draft')),
        ('5hidden', _('status_pending')),
        ('6deleted', _('status_deleted')),
    }

    status = models.CharField(
        max_length=10, choices=BLOG_STATUS, default='1normal')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    category = models.CharField(max_length=23, blank=True)
    title = models.CharField(max_length=41)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    like_users = models.TextField(default='', blank=True)
    image = models.ImageField(
        upload_to="featured_images/%Y-%m/", blank=True)
    tags = models.TextField(default='', blank=True)

    def get_absolute_url(self):
        """Back to list"""
        return reverse_lazy('blogs:show_blogs', args=[1])

    def get_post_url(self):
        """Back to post"""
        return reverse_lazy('blogs:show_post', args=[self.id])

    def get_edit_url(self):
        """Stay editing"""
        return reverse_lazy('blogs:edit_post', args=[self.id])

    def get_status_text(self):
        """Get status text"""
        if self.status == '1normal':
            return _('status_normal')
        elif self.status == '2temp':
            return _('status_draft')
        elif self.status == '5hidden':
            return _('status_pending')
        elif self.status == '6deleted':
            return _('status_deleted')


class Comment(models.Model):
    """Comment of blogs"""

    COMMENT_STATUS = {
        ('1normal', _('status_normal')),
        ('6deleted', _('status_deleted')),
        ('7spam', _('status_spam')),
    }

    post_id = models.IntegerField(default=0)
    comment_id = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10, choices=COMMENT_STATUS, default='1normal')
    userid = models.CharField(max_length=settings.ID_MAX_LENGTH, blank=True)
    username = models.CharField(max_length=settings.USERNAME_MAX, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    content = models.TextField(max_length=settings.COMMENT_TEXT_MAX)
