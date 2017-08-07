# -*- coding: utf-8 -*-
from smtplib import SMTPException
import sys

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from .forms import RegistrationForm, SettingForm, UserInfoForm
from .models import Profile

reload(sys)
sys.setdefaultencoding('utf-8')


def setting(request):
    """Account setting"""
    if request.method == "POST":
        settingform = SettingForm(request.POST)
        if settingform.is_valid():
            setting = settingform.save(commit=False)
            request.user.profile.sense_client = setting.sense_client
            request.user.profile.sense_slot = setting.sense_slot
            request.user.profile.save()
            msg = _('Saved successfully.')
        else:
            msg = _('Form validation Failure')

    elif request.method == "GET":
        if request.user.is_authenticated():
            msg = ""
            settingform = SettingForm(instance=request.user.profile)
        else:
            return redirect('/')

    return render(
        request,
        "accounts/setting.html",
        {
            'settingform': settingform,
            'msg': msg,
        }
    )


def user_info(request):
    """User information"""
    id = request.user.profile.id
    profile = get_object_or_404(Profile, pk=id)
    if request.method == "POST":
        infoform = UserInfoForm(request.POST, request.FILES, instance=profile)
        if infoform.is_valid():
            error = False
            if settings.ENABLE_NICKNAME:
                nick = infoform.cleaned_data['first_name']
                if nick != request.user.first_name:
                    if nick == '':
                        request.user.first_name = ''
                    else:
                        q = Q(username__iexact=nick) \
                            | Q(first_name__iexact=nick)
                        if User.objects.filter(q).exists() or \
                            len(nick) < settings.NICKNAME_MIN_LENGTH or \
                                len(nick) > settings.NICKNAME_MAX_LENGTH:
                                msg = _('Please check nickname.')
                                error = True
                        else:
                            request.user.first_name = nick

            email = infoform.cleaned_data['email']
            if not error and email != request.user.email:
                code = infoform.cleaned_data['code']
                signer = TimestampSigner()
                try:
                    value = signer.unsign(
                        code, max_age=settings.VERIFICATION_CODE_VALID)
                    code_check = value == email

                    if code_check:
                        request.user.email = email
                    else:
                        msg = _('Verification failure. Please check verification code again.')
                        error = True
                except:
                    msg = _('Verification failure. Please check verification code again.')
                    error = True

            if not error:
                msg = _('Saved successfully.')
                request.user.save()
                infoform.save()
        else:
            msg = _('Form validation Failure')
    elif request.method == "GET":
        if request.user.is_authenticated():
            msg = ""
            infoform = UserInfoForm(instance=profile)
        else:
            return redirect('/')

    return render(
        request,
        "accounts/user_info.html",
        {
            'infoform': infoform,
            'username': request.user.username,
            'date_joined': request.user.date_joined,
            'point': profile.point,
            'portrait': profile.portrait,
            'msg': msg,
        }
    )


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

            code = userform.cleaned_data['code']
            email = userform.cleaned_data['email']
            signer = TimestampSigner()

            try:
                value = signer.unsign(
                    code, max_age=settings.VERIFICATION_CODE_VALID)
                code_check = value == email

                if code_check:
                    userform.save()
                    return render(
                        request,
                        "accounts/join.html",
                    )
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
        "accounts/signup.html",
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
