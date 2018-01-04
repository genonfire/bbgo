# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models


class Alias(models.Model):
    """Alias of aliases"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
