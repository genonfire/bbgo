# -*- coding: utf-8 -*-
from smtplib import SMTPException
import sys

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from .forms import RegistrationForm

reload(sys)
sys.setdefaultencoding('utf-8')


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
        "registration/signup.html",
        {
            'userform': userform,
        }
    )


@user_passes_test(lambda u: u.is_superuser)
def send_email(request):
    """Send email to user for testing purpose"""
    id_email = request.user.email
    print "sending email to", id_email
    signer = TimestampSigner()
    value = signer.sign(id_email)
    subject = u'Test email.'
    body = u'keyCode: %s' % value

    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, [id_email], fail_silently=False)
        return HttpResponse("Email sent", status=201)
    except SMTPException:
        return HttpResponse(status=400)
