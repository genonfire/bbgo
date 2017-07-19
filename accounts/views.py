# -*- coding: utf-8 -*-
from smtplib import SMTPException
import sys

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import RegistrationForm

reload(sys)
sys.setdefaultencoding('utf-8')


def check_validation(request):
    """Function"""
    username = request.POST.get('username')
    idcheck = User.objects.filter(username__iexact=username).exists()

    code = request.POST.get('code')
    email = request.POST.get('email')
    signer = TimestampSigner()
    msg = ''
    result = False

    try:
        value = signer.unsign(code, max_age=180)
        code_check = value == email

        if idcheck:
            msg = u"이미 존재하는 아이디입니다."
        elif not code_check:
            msg = u"인증코드가 잘못되었습니다."
        else:
            result = True
    except:
        msg = u"인증코드가 잘못되었습니다."

    data = {
        'result': result,
        'msg': msg,
    }

    return JsonResponse(data)


def sign_up(request):
    """Function"""
    if request.method == "POST":
        userform = RegistrationForm(request.POST)
        if userform.is_valid():
            userform.save(commit=False)
            email = userform.cleaned_data['email']
            code = userform.cleaned_data['code']
            signer = TimestampSigner()
            try:
                value = signer.unsign(code, max_age=86400)
                id_check = value == email
                if (id_check):
                    msg = u"가입성공.<br><a href=%s>로그인</a>" % reverse_lazy('accounts:login')
                    userform.save()
                else:
                    msg = u"인증코드를 확인해 주세요."
            except:
                msg = u"인증코드를 확인해 주세요.."
        else:
            msg = u"회원가입 오류.<br>아이디를 확인해 주세요."
        return HttpResponse(msg)
    elif request.method == "GET":
        userform = RegistrationForm()

    return render(
        request,
        "accounts/signup.html",
        {
            'userform': userform,
        }
    )


def check_duplication(request):
    """Function"""
    username = request.POST.get('username')
    idcheck = User.objects.filter(username__iexact=username).exists()
    if (idcheck):
        msg = u"이미 존재하는 아이디입니다."
    else:
        msg = u"사용 가능한 아이디입니다."
    data = {
        'idcheck': idcheck,
        'msg': msg,
    }
    return JsonResponse(data)


def check_email(request):
    """Function"""
    email = request.POST.get('email')

    if User.objects.filter(email__iexact=email).exists():
        msg = u"이미 존재하는 이메일 주소입니다. 비밀번호 찾기를 이용해 보세요."
        data = {
            'msg': msg,
        }
        return JsonResponse(data, status=201)

    signer = TimestampSigner()
    value = signer.sign(email)
    subject = u'[노룩뉴스] 회원가입 인증 메일입니다.'
    body = u'인증코드(이메일주소 포함): %s' % value

    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        msg = u"인증코드를 이메일로 발송했습니다."
        data = {
            'msg': msg,
        }
        return JsonResponse(data, status=201)
    except SMTPException:
        return JsonResponse({'status': 'false'}, status=400)
