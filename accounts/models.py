# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """User model extension"""

    user = models.OneToOneField(User)
    point = models.IntegerField(default=1)
    last_article_at = models.DateTimeField(auto_now_add=True)
    last_reply_at = models.DateTimeField(auto_now_add=True)
    bookmarks = models.TextField(default='', blank=True)
    scrap = models.TextField(default='', blank=True)
    alarm = models.BooleanField(default=False)
    alarm_list = models.TextField(default='', blank=True)


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
