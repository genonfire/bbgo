# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.utils import get_ipaddress

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def img_validator(attached):
    """Validator to limit file size"""
    size = attached.file.size
    if size > settings.PORTRAIT_SIZE_LIMIT:
        raise ValidationError('image validation failed')


class Profile(models.Model):
    """User model extension"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=1)
    last_article_at = models.DateTimeField(auto_now_add=True)
    last_reply_at = models.DateTimeField(auto_now_add=True)
    suspension_till = models.DateTimeField(auto_now_add=True, blank=True)
    bookmarks = models.TextField(default='', blank=True)
    scrap = models.TextField(default='', blank=True)
    alarm = models.BooleanField(default=False)
    msg_count = models.IntegerField(default=0)
    alarm_list = models.TextField(default='', blank=True)
    ip_list = models.TextField(default='', blank=True)
    sense_client = models.CharField(max_length=30, blank=True)
    sense_slot = models.CharField(max_length=15, blank=True)
    id1 = models.CharField(max_length=30, blank=True)
    id2 = models.CharField(max_length=30, blank=True)
    id3 = models.CharField(max_length=30, blank=True)
    alarm_interval = models.IntegerField(
        default=settings.DEFAULT_ALARM_INTERVAL)
    alarm_board = models.BooleanField(default=False)
    alarm_reply = models.BooleanField(default=True)
    alarm_team = models.BooleanField(default=False)
    alarm_full = models.BooleanField(default=True)
    portrait = models.ImageField(
        upload_to="portrait/%Y-%m-%d/", blank=True, validators=[img_validator])
    signature = models.TextField(blank=True)


class UserSession(models.Model):
    """User key for Session"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create signal"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update signal"""
    if Profile.objects.filter(user=instance):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)


def user_logged_in_signal(sender, user, request, **kwargs):
    """user_logged_in_signal"""
    ip = get_ipaddress(request)
    ip_list = user.profile.ip_list.split(',')

    if ip not in ip_list:
        if user.profile.ip_list != '':
            user.profile.ip_list += ","
        user.profile.ip_list += ip
    user.profile.save()

    UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key
    )


user_logged_in.connect(user_logged_in_signal)  # login signal
