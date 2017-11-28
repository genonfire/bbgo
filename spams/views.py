# -*- coding: utf-8 -*-
from core.utils import error_to_response, get_referrer, get_useragent
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils import timezone
import requests

from .forms import SpamIPEditForm, SpamWordEditForm
from .models import IP, Word


def akismet_comment_check(request, comment):
    """Akismet comment check"""
    if settings.ENABLE_AKISMET:
        url_verify_key = 'https://rest.akismet.com/1.1/verify-key'
        key = settings.AKISMET_API_KEY
        blog = settings.BLOG_URL
        data = {'key': key, 'blog': blog}

        response = requests.post(url_verify_key, data=data)
        if response.text == 'valid':
            url = 'https://%s.rest.akismet.com/1.1/comment-check' % key
            data = {
                'blog': blog,
                'user_ip': comment.ip,
                'user_agent': get_useragent(request),
                'referrer': get_referrer(request),
                'comment_type': 'comment',
                'comment_author': comment.username,
                'comment_content': comment.content,
                'comment_date_gmt': timezone.now(),
                'blog_lang': settings.LANGUAGE_CODE,
                'blog_charset': 'UTF-8',
            }

            result = requests.post(url, data=data)
            if result.text == 'true':
                return True
    return False


def check_spam(request, comment):
    """Check spam"""
    ip = comment.ip
    ip_exist = IP.objects.filter(ip__iexact=ip).exists()
    if ip_exist:
        return True

    words = Word.objects.all()
    for word in words:
        if word.word in comment.content:
            return True

    if settings.ENABLE_AKISMET:
        is_spam = akismet_comment_check(request, comment)
        if is_spam:
            return True

    return False


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
