#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

class Board(models.Model):
    table = models.CharField(max_length="30", choices=settings.BOARD_TABLES, default='0')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    datetime = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    category = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    viewcount = models.IntegerField(default=0)
    likecount = models.IntegerField(default=0)
    likeusers = models.TextField(default='')

    def get_absolute_url(self):
        return reverse_lazy('board show list', args=[self.table])
