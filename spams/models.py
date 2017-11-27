# -*- coding: utf-8 -*-
from django.db import models


class IP(models.Model):
    """IP address of spams"""

    ip = models.GenericIPAddressField()


class Word(models.Model):
    """Word of spams"""

    word = models.CharField(max_length=50)
