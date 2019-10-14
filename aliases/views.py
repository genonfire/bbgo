# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.utils import error_page, error_to_response

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.utils.translation import ugettext as _

from .forms import AliasEditForm
from .models import Alias


@login_required
def dashboard(request):
    """Dashboard"""
    return render(
        request,
        "aliases/dashboard.html",
        {
        }
    )


def click(request, alias):
    """Click alias"""
    a = Alias.objects.filter(name__exact=alias)
    if a:
        a[0].clicks += 1
        a[0].save()
        return redirect(a[0].url)
    else:
        errormsg = _('The page you requested is not exist. Please try something else.')
        return error_page(request, errormsg)


@login_required
def new_alias(request):
    """API new_alias"""
    if request.method == 'POST':
        name = request.POST['name']
        exist = Alias.objects.filter(name__exact=name).exists()
        if exist is True:
            return JsonResponse({'status': 'false'}, status=412)

        form = AliasEditForm(request.POST)
        if form.is_valid():
            alias = form.save(commit=False)
            alias.user = request.user
            alias.save()

            aliases = Alias.objects.filter(user=request.user).all()
            return render_to_response(
                'aliases/show_aliases.html',
                {
                    'aliases': aliases,
                }
            )
        else:
            return JsonResponse({'status': 'false'}, status=400)
    else:
        return error_to_response(request)


@login_required
def edit_alias(request):
    """API edit_alias"""
    if request.method == 'POST':
        id = request.POST['id']
        url = request.POST['url']
        user = request.user
        alias = get_object_or_404(Alias, pk=id)

        if user != alias.user:
            return JsonResponse({'status': 'false'}, status=400)

        if url == alias.url:
            return JsonResponse({'status': 'false'}, status=412)
        else:
            alias.url = url
            alias.save()
            aliases = Alias.objects.filter(user=user).all()

            return render_to_response(
                'aliases/show_aliases.html',
                {
                    'aliases': aliases,
                }
            )
    else:
        return error_to_response(request)


@login_required
def delete_alias(request):
    """API delete_alias"""
    if request.method == 'POST':
        id = request.POST['id']
        user = request.user
        alias = get_object_or_404(Alias, pk=id)

        if user != alias.user:
            return JsonResponse({'status': 'false'}, status=400)

        alias.delete()
        aliases = Alias.objects.filter(user=user).all()

        return render_to_response(
            'aliases/show_aliases.html',
            {
                'aliases': aliases,
            }
        )
    else:
        return error_to_response(request)
