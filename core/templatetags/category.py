# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

from recipes.models import Category

register = template.Library()


@register.inclusion_tag('recipes/show_category.html', takes_context=True)
def show_category(context):
    """Show category"""
    categories = Category.objects.order_by('order')

    return {
        'categories': categories,
        'category_length': settings.RECIPE_CATEGORY_MAX,
    }
