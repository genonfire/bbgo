# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Category, Recipe


class CategoryEditForm(forms.ModelForm):
    """Category for recipes"""

    class Meta:
        """Meta for CategoryEditForm"""

        model = Category
        fields = ('name',)


class RecipeEditForm(forms.ModelForm):
    """Recipe for recipes"""

    class Meta:
        """Meta for RecipeEditForm"""

        model = Recipe
        exclude = ('order', )
