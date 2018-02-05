# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models


class Category(models.Model):
    """Category of recipes"""

    name = models.CharField(max_length=settings.RECIPE_CATEGORY_MAX)
    order = models.IntegerField(default=1)


class Recipe(models.Model):
    """Recipe of recipes"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=settings.RECIPE_NAME_MAX)
    order = models.IntegerField(default=1)
    recipe = models.TextField()
    image = models.ImageField(upload_to="recipes/", blank=True)

    def delete(self, *args, **kwargs):
        """To delete attached too"""
        self.image.delete()
        super(Recipe, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        """Back to list"""
        return reverse_lazy('recipes:show_recipes')
