# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.utils import error_page, is_mobile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _

from .forms import CheckKeyForm, KeyEditForm, NewKeyForm, VaultEditForm
from .models import Key, Vault


@login_required
def check_seal(request):
    """Check seal"""
    if settings.ENABLE_MASTERKEY:
        opened = Key.objects.filter(user=request.user).exists()
        return opened
    else:
        return True


@login_required
def key_expired(request):
    """Check key expiry"""
    if settings.ENABLE_MASTERKEY:
        key = Key.objects.filter(user=request.user).latest('created_at')
        now = timezone.now()
        if now > key.expiry:
            return True, 0
        else:
            return False, int((key.expiry - now).total_seconds())
    else:
        return False, 0


@login_required
def check_key(request):
    """Check masterkey"""
    if not settings.ENABLE_MASTERKEY:
        return redirect('vaults:open_vault')
    if not check_seal(request):
        return redirect('vaults:new_key')

    msg = ''
    if request.method == "POST":
        checkform = CheckKeyForm(request.POST)
        if checkform.is_valid():
            inputkey = checkform.save(commit=False)
            key = Key.objects.filter(user=request.user).latest('created_at')
            if check_password(inputkey.masterkey, key.masterkey):
                key.expiry = timezone.now() + timezone.timedelta(
                    minutes=settings.MASTERKEY_SESSION_TIME)
                key.save()
                return redirect(key.get_absolute_url())
            else:
                msg = _('Wrong master key.')
    elif request.method == "GET":
        checkform = CheckKeyForm()

    return render(
        request,
        "vaults/check_key.html",
        {
            'form': checkform,
            'msg': msg,
        }
    )


@login_required
def new_key(request):
    """New key"""
    if not settings.ENABLE_MASTERKEY:
        return redirect('vaults:open_vault')
    if check_seal(request):
        return redirect('vaults:open_vault')

    if request.method == "POST":
        editform = NewKeyForm(request.POST)
        if editform.is_valid():
            key = editform.save(commit=False)
            key.user = request.user
            key.masterkey = make_password(key.masterkey)
            key.save()

            return redirect(key.get_absolute_url())
    elif request.method == "GET":
        editform = NewKeyForm()

    return render(
        request,
        "vaults/new_key.html",
        {
            'form': editform,
        }
    )


@login_required
def edit_key(request):
    """Edit key"""
    if not settings.ENABLE_MASTERKEY:
        return redirect('vaults:open_vault')
    if not check_seal(request):
        return redirect('vaults:new_key')

    msg = ''
    key = Key.objects.filter(user=request.user).latest('created_at')

    if request.method == "POST":
        editform = KeyEditForm(request.POST)
        if editform.is_valid():
            newkey = editform.save(commit=False)
            current_key = editform.cleaned_data['current_key']

            if check_password(current_key, key.masterkey):
                key.masterkey = make_password(newkey.masterkey)
                key.created_at = timezone.now()
                key.save()
                return redirect(key.get_absolute_url())
            else:
                msg = _('Wrong master key.')
    elif request.method == "GET":
        editform = KeyEditForm()

    return render(
        request,
        "vaults/edit_key.html",
        {
            'form': editform,
            'msg': msg,
        }
    )


@login_required
def open_vault(request, category='all'):
    """Open vault"""
    if not check_seal(request):
        return redirect('vaults:new_key')

    expired, expiry = key_expired(request)
    if expired:
        return check_key(request)

    if category == 'all':
        q = Q(user=request.user)
    else:
        q = Q(user=request.user) & Q(category__iexact=category)

    vaults = Vault.objects.filter(q).order_by('category', 'order')
    mobile = is_mobile(request)

    return render(
        request,
        "vaults/show_vault.html",
        {
            'vaults': vaults,
            'category': category,
            'expiry': expiry,
            'mobile': mobile,
        }
    )


@login_required
def new_vault(request):
    """New vault"""
    if not check_seal(request):
        return redirect('vaults:new_key')

    expired, expiry = key_expired(request)
    if expired:
        return check_key(request)

    if request.method == "POST":
        editform = VaultEditForm(request.POST, request.FILES)
        if editform.is_valid():
            vault = editform.save(commit=False)
            vault.user = request.user
            try:
                latest = Vault.objects.latest('id')
                vault.order = latest.id + 1
            except ObjectDoesNotExist:
                vault.order = 1
            vault.save()

            return redirect(vault.get_absolute_url())
    elif request.method == "GET":
        editform = VaultEditForm()

    return render(
        request,
        "vaults/edit_vault.html",
        {
            'form': editform,
            'edit_type': 'new',
            'expiry': expiry,
        }
    )


@login_required
def edit_vault(request, id):
    """Edit vault"""
    if not check_seal(request):
        return redirect('vaults:new_key')

    expired, expiry = key_expired(request)
    if expired:
        return check_key(request)

    vault = get_object_or_404(Vault, pk=id)
    if vault.user != request.user:
        return error_page(request)

    if request.method == "POST":
        editform = VaultEditForm(request.POST, request.FILES, instance=vault)
        if editform.is_valid():
            vault = editform.save(commit=False)
            vault.save()

            return redirect(vault.get_absolute_url())
    elif request.method == "GET":
        editform = VaultEditForm(instance=vault)

    return render(
        request,
        "vaults/edit_vault.html",
        {
            'form': editform,
            'edit_type': 'edit',
            'vault': vault,
            'expiry': expiry,
        }
    )


@login_required
def delete_vault(request, id):
    """Delete vault"""
    vault = get_object_or_404(Vault, pk=id)
    if vault.user != request.user:
        return error_page(request)

    vault.delete()
    return redirect(vault.get_absolute_url())


@login_required
def save_order(request):
    """API save_order"""
    if request.method == 'POST':
        orders = dict(request.POST.iterlists())['order[]']

        for index, order in enumerate(orders):
            vault = get_object_or_404(Vault, pk=order)
            vault.order = index + 1
            vault.save()

        return JsonResponse({'status': 'true'}, status=201)

    return error_page(request)


@login_required
def extend_expiry(request):
    """API extend_expiry"""
    if request.method == "POST":
        if not settings.ENABLE_MASTERKEY:
            return JsonResponse({'status': 'false'}, status=400)
        expired, expiry = key_expired(request)
        if expired:
            return JsonResponse({'status': 'false'}, status=400)
        else:
            key = Key.objects.filter(user=request.user).latest('created_at')
            key.expiry = timezone.now() + timezone.timedelta(
                minutes=settings.MASTERKEY_SESSION_TIME)
            key.save()
            expiry_sec = settings.MASTERKEY_SESSION_TIME * 60
            return JsonResponse([expiry_sec], safe=False, status=201)

    return error_page(request)
