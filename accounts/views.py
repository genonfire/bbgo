# -*- coding: utf-8 -*-
from math import ceil
import re
from smtplib import SMTPException

from boards.models import Board, Reply
from boards.table import BoardTable
from core.utils import error_page

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from .forms import RegistrationForm, SettingForm, UserInfoForm
from .models import Profile


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


def edit_user_info(request):
    """Edit user information"""
    if not request.user.is_authenticated():
        return redirect('/')

    profile = get_object_or_404(Profile, pk=request.user.profile.id)
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
        "accounts/edit_user_info.html",
        {
            'infoform': infoform,
            'username': request.user.username,
            'date_joined': request.user.date_joined,
            'point': profile.point,
            'portrait': profile.portrait,
            'msg': msg,
        }
    )


def user_info(request, user):
    """Show user info"""
    if not request.user.is_authenticated():
        msg = _("Require login")
        return error_page(request, msg)

    userinfo = User.objects.filter(username__iexact=user).get()
    article_no = Board.objects.filter(user__username__iexact=user).count()
    reply_no = Reply.objects.filter(user__username__iexact=user).count()

    return render(
        request,
        "accounts/user_info.html",
        {
            'userinfo': userinfo,
            'article_no': article_no,
            'reply_no': reply_no,
        }
    )


def scrap(request, page=0):
    """Show my scrap"""
    if not request.user.is_authenticated():
        return redirect('/')

    if int(page) < 1:
        return redirect('accounts:scrap', page=1)

    board_table = BoardTable()
    my_scrap = []
    name_list = board_table.get_table_list()
    list_count = board_table.get_list_count()

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    q = Q(status__iexact='1normal') | Q(status__iexact='4warning')

    scrap = request.user.profile.scrap.split(',')
    total = len(scrap)

    if request.user.profile.scrap != '':
        for index, s in enumerate(scrap[start_at:end_at]):
            app, id = s.split(':')
            if app == 'boards':
                item = Board.objects.filter(id__iexact=id).filter(q)
                if item.count():
                    my_scrap.append([item[0]])
            else:
                continue

    index_total = int(ceil(float(total) / list_count))
    index_begin = (current_page / 10) * 10 + 1
    index_end = mindex_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9
    mindex_begin = (current_page / 5) * 5 + 1
    if mindex_end - mindex_begin >= 5:
        mindex_end = mindex_begin + 4

    return render(
        request,
        "accounts/scrap.html",
        {
            'my_scrap': my_scrap,
            'total': total,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'mindex_begin': mindex_begin,
            'mindex_end': mindex_end + 1,
            'index_total': index_total,
            'name_list': name_list,
        }
    )


def delete_scrap(request, id):
    """Delete selected scrap"""
    profile = request.user.profile
    app_id = 'boards:' + id
    regstr = re.escape(app_id) + r"\b(,|)"
    profile.scrap = re.sub(regstr, '', profile.scrap)
    if profile.scrap and profile.scrap[-1] == ',':
        profile.scrap = profile.scrap[:-1]

    request.user.profile.save()
    return redirect('accounts:scrap_0')


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
                return error_page(request, msg)

            if settings.ENABLE_NICKNAME:
                nick = userform.cleaned_data['first_name']
                if nick:
                    q = Q(username__iexact=nick) | Q(first_name__iexact=nick)
                    if User.objects.filter(q).exists() or \
                        len(nick) < settings.NICKNAME_MIN_LENGTH or \
                            len(nick) > settings.NICKNAME_MAX_LENGTH:
                        msg = _('Please check nickname.')
                        return error_page(request, msg)

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

        return error_page(request, msg)
    elif request.method == "GET":
        userform = RegistrationForm()

    return render(
        request,
        "accounts/signup.html",
        {
            'userform': userform,
        }
    )


def show_deactivate_account(request):
    """Show deactivate account page"""
    return render(
        request,
        "accounts/deactivate_account.html"
    )


def deactivate_account(request):
    """Deactivate account"""
    if request.user.is_authenticated():
        request.user.is_active = False
        if request.user.is_staff:
            request.user.is_staff = False
        request.user.save()

    return redirect(reverse_lazy('accounts:logout'))


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
        return error_page(request, "Email sent", status=201)
    except SMTPException:
        return error_page(request, "Error!")
