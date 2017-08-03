# -*- coding: utf-8 -*-
from smtplib import SMTPException
import sys

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from .forms import RegistrationForm

reload(sys)
sys.setdefaultencoding('utf-8')


def sign_up(request):
    """Sign up"""
    if request.method == "POST":
        userform = RegistrationForm(request.POST)
        if userform.is_valid():
            userform.save(commit=False)

            username = userform.cleaned_data['username']
            q = Q(username__iexact=username) | Q(first_name__iexact=username)
            if User.objects.filter(q).exists() or \
                len(username) < settings.ID_MIN_LENGTH or \
                    len(username) > settings.ID_MAX_LENGTH:
                msg = _('Please check username.')
                return HttpResponse(msg)

            if settings.ENABLE_NICKNAME:
                nick = userform.cleaned_data['first_name']
                if nick:
                    q = Q(username__iexact=nick) | Q(first_name__iexact=nick)
                    if User.objects.filter(q).exists() or \
                        len(nick) < settings.NICKNAME_MIN_LENGTH or \
                            len(nick) > settings.NICKNAME_MAX_LENGTH:
                        msg = _('Please check nickname.')
                        return HttpResponse(msg)

            email = userform.cleaned_data['email']
            code = userform.cleaned_data['code']
            signer = TimestampSigner()
            try:
                value = signer.unsign(code, max_age=86400)  # 24 hours
                code_check = value == email

                if code_check:
                    msg = u"%s.<br><a href=%s>%s</a>" % (
                        _('Thank you for joining us.'),
                        reverse_lazy('accounts:login'),
                        _('login')
                    )
                    userform.save()
                else:
                    msg = _('Verification failure. Please check verification code again.')
            except:
                msg = _('Verification failure. Please check verification code again.')
        else:
            msg = _('Sorry. Please try again later.')

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
