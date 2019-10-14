# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Category, Recipe

admin.site.register(Category)
admin.site.register(Recipe)
