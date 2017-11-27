# -*- coding: utf-8 -*-
from core.utils import error_to_response, get_ipaddress
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response

from .forms import SpamIPEditForm, SpamWordEditForm
from .models import IP, Word


def check_spam(request, comment):
    """Check spam"""
    ip = get_ipaddress(request)

    ip_exist = IP.objects.filter(ip__iexact=ip).exists()
    word_exist = False

    words = Word.objects.all()
    for word in words:
        if word.word in comment.content:
            word_exist = True
            break

    return ip_exist, word_exist


@staff_member_required
def setting(request):
    """Spam setting"""
    return render(
        request,
        "spams/spam_setting.html",
        {
        }
    )


@staff_member_required
def add_ip(request):
    """API add_ip"""
    if request.method == 'POST':
        ip = request.POST['ip']
        exist = IP.objects.filter(ip__iexact=ip).exists()
        if exist is True:
            return JsonResponse({'status': 'false'}, status=412)

        form = SpamIPEditForm(request.POST)
        if form.is_valid():
            form.save()
            ips = IP.objects.all()

            return render_to_response(
                'spams/show_ips.html',
                {
                    'ips': ips,
                }
            )
        else:
            return JsonResponse({'status': 'false'}, status=500)

    else:
        return error_to_response(request)


@staff_member_required
def delete_ip(request):
    """API delete_ip"""
    if request.method == 'POST':
        id = request.POST['id']
        ip = get_object_or_404(IP, pk=id)
        ip.delete()
        ips = IP.objects.all()

        return render_to_response(
            'spams/show_ips.html',
            {
                'ips': ips,
            }
        )
    else:
        return error_to_response(request)


@staff_member_required
def add_word(request):
    """API add_word"""
    if request.method == 'POST':
        word = request.POST['word']
        exist = Word.objects.filter(word__iexact=word).exists()
        if exist is True:
            return JsonResponse({'status': 'false'}, status=412)

        form = SpamWordEditForm(request.POST)
        if form.is_valid():
            form.save()
            words = Word.objects.all()

            return render_to_response(
                'spams/show_words.html',
                {
                    'words': words,
                }
            )
        else:
            return JsonResponse({'status': 'false'}, status=500)

    else:
        return error_to_response(request)


@staff_member_required
def delete_word(request):
    """API delete_word"""
    if request.method == 'POST':
        id = request.POST['id']
        word = get_object_or_404(Word, pk=id)
        word.delete()
        words = Word.objects.all()

        return render_to_response(
            'spams/show_words.html',
            {
                'words': words,
            }
        )
    else:
        return error_to_response(request)


@staff_member_required
def register_ip(request):
    """API register_ip"""
    if request.method == 'POST':
        ip = request.POST['ip']
        exist = IP.objects.filter(ip__iexact=ip).exists()
        if exist is True:
            return JsonResponse({'status': 'false'}, status=412)

        form = SpamIPEditForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'true'}, status=201)
        else:
            return JsonResponse({'status': 'false'}, status=500)

    else:
        return JsonResponse({'status': 'false'}, status=400)
