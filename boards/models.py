# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext as _


class Board(models.Model):
    """Board of boards"""

    BOARD_STATUS = {
        ('1normal', _('status_normal')),
        ('2temp', _('status_temp')),
        ('3notice', _('status_notice')),
        ('4warning', _('status_warning')),
        ('5hidden', _('status_hidden')),
        ('6deleted', _('status_deleted')),
    }

    table = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=BOARD_STATUS, default='1normal')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    category = models.CharField(max_length=23, blank=True)
    subject = models.CharField(max_length=41)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name="board_like_users")
    dislike_users = models.ManyToManyField(
        User, related_name="board_dislike_users")
    reference = models.CharField(max_length=1855, default='', blank=True)
    has_image = models.BooleanField(default=False)
    has_video = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Back to list"""
        return reverse_lazy('boards:show_list_0', args=[self.table])

    def get_article_url(self):
        """Back to article"""
        return reverse_lazy('boards:show_article', args=[self.id])

    def get_status_text(self):
        """Get status text"""
        if self.status == '1normal':
            return _('status_normal')
        elif self.status == '2temp':
            return _('status_temp')
        elif self.status == '3notice':
            return _('status_notice')
        elif self.status == '4warning':
            return _('status_warning')
        elif self.status == '5hidden':
            return _('status_hidden')
        elif self.status == '6deleted':
            return _('status_deleted')

    def get_image_text(self):
        """Get image text"""
        return '<img src="/upload/django-summernote/'

    def get_video_text(self):
        """Get video text"""
        return '<iframe frameborder="0" src="//www.youtube.com/'


class Reply(models.Model):
    """Reply of boards"""

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
    image = models.ImageField(upload_to="reply-images/%Y-%m-%d/", blank=True)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name="reply_like_users")
    dislike_users = models.ManyToManyField(
        User, related_name="reply_dislike_users")
