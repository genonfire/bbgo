# -*- coding: utf-8 -*-
import sys

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

reload(sys)
sys.setdefaultencoding('utf-8')


class Profile(models.Model):
    """User model extension"""

    user = models.OneToOneField(User)
    point = models.IntegerField(default=1)


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
