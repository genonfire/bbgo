# -*- coding: utf-8 -*-
from random import randint

from core.utils import error_page
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import redirect, render
from django.template import RequestContext

from .forms import CategoryEditForm, RecipeEditForm
from .models import Category, Recipe


def instruction(request):
    """Show instruction"""
    return render(
        request,
        "recipes/instruction.html",
    )


def show_recipes(request, category=''):
    """Show recipes"""
    categories = Category.objects.order_by('order')
    if categories.count() == 0:
        return redirect('recipes:instruction')

    if category:
        q = Q(category__id__iexact=category)
    else:
        q = Q()

    recipes = Recipe.objects.filter(q).order_by('category__order', 'order')
    if category:
        category = int(category)

    return render(
        request,
        "recipes/show_recipes.html",
        {
            'categories': categories,
            'recipes': recipes,
            'category': category,
        }
    )


def what_today(request):
    """What today?"""
    if request.method == "POST":
        category = request.POST['category']
        if category:
            q = Q(category__id__iexact=category)
        else:
            q = Q()

        count = Recipe.objects.filter(q).count()
        if count:
            recipes = Recipe.objects.filter(q)
            random = randint(0, count - 1)
            recipe = recipes[random]
            return JsonResponse([recipe.id], safe=False, status=201)
        else:
            return JsonResponse({'status': 'false'}, status=400)

    return error_page(request)


@user_passes_test(lambda u: u.is_superuser)
def new_recipe(request):
    """New recipe"""
    categories = ''

    if request.method == "POST":
        editform = RecipeEditForm(request.POST, request.FILES)
        if editform.is_valid():
            recipe = editform.save(commit=False)
            try:
                latest = Recipe.objects.latest('id')
                recipe.order = latest.id + 1
            except ObjectDoesNotExist:
                recipe.order = 1

            recipe.save()
            return redirect(recipe.get_absolute_url())
    elif request.method == "GET":
        editform = RecipeEditForm()
        categories = Category.objects.order_by('order')

    return render(
        request,
        "recipes/edit_recipe.html",
        {
            'form': editform,
            'edit_type': 'new',
            'categories': categories,
        }
    )


@user_passes_test(lambda u: u.is_superuser)
def edit_recipe(request, id):
    """Edit recipe"""
    categories = ''
    recipe = get_object_or_404(Recipe, pk=id)

    if request.method == "POST":
        editform = RecipeEditForm(request.POST, request.FILES, instance=recipe)
        if editform.is_valid():
            recipe = editform.save(commit=False)
            recipe.save()

            return redirect(recipe.get_absolute_url())
    elif request.method == "GET":
        editform = RecipeEditForm(instance=recipe)
        categories = Category.objects.order_by('order')

    return render(
        request,
        "recipes/edit_recipe.html",
        {
            'form': editform,
            'edit_type': 'edit',
            'recipe': recipe,
            'categories': categories,
        }
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_recipe(request, id):
    """Delete recipe"""
    recipe = get_object_or_404(Recipe, pk=id)
    recipe.delete()
    return redirect(recipe.get_absolute_url())


@user_passes_test(lambda u: u.is_superuser)
def save_order(request):
    """Save order"""
    if request.method == "POST":
        orders = dict(request.POST.iterlists())['order[]']
        for index, order in enumerate(orders):
            recipe = get_object_or_404(Recipe, pk=order)
            recipe.order = index + 1
            recipe.save()

        return JsonResponse({'status': 'true'}, status=201)

    return error_page(request)


@user_passes_test(lambda u: u.is_superuser)
def edit_category(request):
    """Edit cateogry"""
    categories = Category.objects.order_by('order')
    return render(
        request,
        "recipes/edit_category.html",
        {
            'categories': categories,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def new_category(request):
    """API new_cateogry"""
    if request.method == "POST":
        editform = CategoryEditForm(request.POST)
        if editform.is_valid():
            category = editform.save(commit=False)
            try:
                latest = Category.objects.latest('id')
                category.order = latest.id + 1
            except ObjectDoesNotExist:
                category.order = 1

            category.save()
            categories = Category.objects.order_by('order')

            return render_to_response(
                "recipes/show_category.html",
                {
                    'categories': categories,
                    'category_length': settings.RECIPE_CATEGORY_MAX,
                },
                context_instance=RequestContext(request)
            )

    return error_page(request)


@user_passes_test(lambda u: u.is_superuser)
def delete_category(request):
    """API delete_category"""
    id = request.POST['id']
    category = get_object_or_404(Category, pk=id)
    category.delete()

    categories = Category.objects.order_by('order')

    return render_to_response(
        "recipes/show_category.html",
        {
            'categories': categories,
            'category_length': settings.RECIPE_CATEGORY_MAX,
        },
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def save_category(request):
    """API save_category"""
    if request.method == "POST":
        orders = dict(request.POST.iterlists())['order[]']
        for index, order in enumerate(orders):
            id, name = order.split(':')
            category = get_object_or_404(Category, pk=id)
            if category.name != name:
                category.name = name
            category.order = index + 1
            category.save()

    categories = Category.objects.order_by('order')

    return render_to_response(
        "recipes/show_category.html",
        {
            'categories': categories,
            'category_length': settings.RECIPE_CATEGORY_MAX,
        },
        context_instance=RequestContext(request)
    )
