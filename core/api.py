# -*- coding: utf-8 -*-
import re
from smtplib import SMTPException

from boards.forms import ReplyEditForm
from boards.models import Board, Reply
from boards.table import BoardTable
from core.utils import error_page, get_ipaddress

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.db.models import Case, IntegerField, When
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone
from django.utils.translation import ugettext as _


def check_duplication(request):
    """API check_duplication"""
    check_type = request.POST.get('check_type')
    name = request.POST.get('username')

    if check_type == 'id':
        min_limit = settings.ID_MIN_LENGTH
        max_limit = settings.ID_MAX_LENGTH
    else:
        min_limit = settings.NICKNAME_MIN_LENGTH
        max_limit = settings.NICKNAME_MAX_LENGTH

    q = Q(username__iexact=name) | Q(first_name__iexact=name)
    idcheck = User.objects.filter(q).exists()

    length = len(name)
    if length < min_limit or length > max_limit:
        return JsonResponse({'status': 'false'}, status=400)

    if request.user.is_authenticated() and idcheck:
        if name == request.user.username or name == request.user.first_name:
            idcheck = False

    if idcheck:
        msg = _('Already exist.')
    else:
        msg = _('Available')

    data = {
        'idcheck': idcheck,
        'msg': msg,
    }

    return JsonResponse(data)


def get_verification_code(request):
    """API get_verification_code"""
    email = request.POST.get('email')

    if User.objects.filter(email__iexact=email).exists():
        msg = _('E-mail exists. Why don\'t you try to find your password?')
        data = {
            'result': False,
            'msg': msg,
        }
        return JsonResponse(data, status=201)

    signer = TimestampSigner()
    value = signer.sign(email)
    subject = _('[%(site_name)s] Verification code for signing in') % {
        'site_name': settings.SITE_NAME
    }
    body = value

    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        msg = _('Verification code sent. Please check your E-mail.')
        data = {
            'result': True,
            'msg': msg,
        }
        return JsonResponse(data, status=201)
    except SMTPException:
        return JsonResponse({'status': 'false'}, status=400)


def check_validation(request):
    """API check_validation"""
    code = request.POST.get('code')
    email = request.POST.get('email')
    signer = TimestampSigner()

    try:
        value = signer.unsign(code, max_age=settings.VERIFICATION_CODE_VALID)
        code_check = value == email

        if code_check:
            return JsonResponse({'status': 'true'}, status=201)
    except:
        pass

    return JsonResponse({'status': 'false'}, status=400)


def like_article(request, liketype):
    """API like_article"""
    if request.method == 'POST':
        if not request.user.is_authenticated():
            msg = _("Require login")
            return JsonResponse([0, msg], safe=False, status=201)

        id = request.POST['id']
        user = request.user.username
        article = get_object_or_404(Board, pk=id)

        if article.user.username == user:
            msg = _("You like your own post?")
            return JsonResponse([0, msg], safe=False, status=201)

        like_users = article.like_users.split(',')
        dislike_users = article.dislike_users.split(',')

        if user not in like_users and user not in dislike_users:
            if liketype == 'like':
                if article.like_users != '':
                    article.like_users += ","
                article.like_users += user
                article.like_count += 1
                article.save()

                msg = _("You've liked this article")
                return JsonResponse(
                    [article.like_count, msg], safe=False, status=201)
            elif liketype == 'dislike':
                if article.dislike_users != '':
                    article.dislike_users += ","
                article.dislike_users += user
                article.dislike_count += 1
                article.save()

                msg = _("You've disliked this article")
                return JsonResponse(
                    [article.dislike_count, msg], safe=False, status=201)
            else:
                return JsonResponse({'status': 'false'}, status=400)
        else:
            if user in like_users:
                msg = _("You've already liked")
            else:
                msg = _("You've already disliked")
            return JsonResponse([0, msg], safe=False, status=201)
    else:
        return error_page(request)


def like_users(request, liketype):
    """API like_users"""
    if request.method == 'POST':
        id = request.POST['id']
        article = get_object_or_404(Board, pk=id)

        if liketype == 'like':
            user_list = article.like_users
        elif liketype == 'dislike':
            user_list = article.dislike_users
        else:
            return JsonResponse({'status': 'false'}, status=400)

        return JsonResponse([user_list], safe=False, status=201)

    else:
        return error_page(request)


def like_reply(request, liketype):
    """API like_reply"""
    if request.method == 'POST':
        if not request.user.is_authenticated():
            msg = _("Require login")
            return JsonResponse([0, msg], safe=False, status=201)

        id = request.POST['id']
        user = request.user.username
        reply = get_object_or_404(Reply, pk=id)

        if reply.user.username == user:
            msg = _("You like your own post?")
            return JsonResponse([0, msg], safe=False, status=201)

        like_users = reply.like_users.split(',')
        dislike_users = reply.dislike_users.split(',')

        if user not in like_users and user not in dislike_users:
            if liketype == 'like':
                if reply.like_users != '':
                    reply.like_users += ","
                reply.like_users += user
                reply.like_count += 1
                reply.save()

                return JsonResponse([reply.like_count], safe=False, status=201)
            elif liketype == 'dislike':
                if reply.dislike_users != '':
                    reply.dislike_users += ","
                reply.dislike_users += user
                reply.dislike_count += 1
                reply.save()

                return JsonResponse(
                    [reply.dislike_count], safe=False, status=201)
            else:
                return JsonResponse({'status': 'false'}, status=400)
        else:
            if user in like_users:
                msg = _("You've already liked")
            else:
                msg = _("You've already disliked")
            return JsonResponse([0, msg], safe=False, status=201)

        return JsonResponse(status=201)
    else:
        return error_page(request)


def write_reply(request):
    """API write_reply"""
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        id = request.POST['article_id']
        reply_id = int(request.POST['reply_id'])
        reply_to = ''

        form = ReplyEditForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            parent_id = reply_id

            while parent_id != 0:
                parent = get_object_or_404(Reply, pk=parent_id)
                if parent:
                    if parent_id == reply_id and request.user != parent.user:
                        reply_to = parent.user.username
                    parent_id = parent.reply_id
                    if parent_id == 0:
                        reply_id = parent.id
                else:
                    return JsonResponse({'status': 'false'}, status=400)

            reply.reply_id = reply_id
            reply.reply_to = reply_to
            reply.status = '1normal'
            reply.user = request.user
            reply.ip = get_ipaddress(request)
            reply.save()

            article = get_object_or_404(Board, pk=id)
            article.reply_count += 1

            if article.user != request.user and reply_id == 0:
                if article.user.profile.alarm_list != '':
                    article.user.profile.alarm_list += ','
                alarm_text = 'b:%d' % article.id
                article.user.profile.alarm_list += alarm_text

                if article.user.profile.alarm_board:
                    article.user.profile.alarm = True
                    article.user.profile.save()
            elif reply_to != request.user.username and reply_id > 0:
                user = User.objects.filter(username=reply_to)
                if user:
                    if user[0].profile.alarm_list != '':
                        user[0].profile.alarm_list += ','
                    alarm_text = 'r:%d' % reply_id
                    user[0].profile.alarm_list += alarm_text

                    if user[0].profile.alarm_reply:
                        user[0].profile.alarm = True
                        user[0].save()

            article.save()

            request.user.profile.last_reply_at = timezone.now()
            request.user.profile.save()

            replies = Reply.objects.filter(article_id=id).annotate(
                custom_order=Case(
                    When(reply_id=0, then='id'),
                    default='reply_id',
                    output_field=IntegerField(),
                )
            ).order_by('custom_order', 'id')

            return render_to_response(
                'boards/show_reply.html',
                {
                    'user': request.user,
                    'article_user': article.user,
                    'replies': replies,
                    'count': replies.count()
                }
            )

        return JsonResponse({'status': 'false'}, status=400)
    else:
        return error_page(request)


def reload_reply(request):
    """API reload_reply"""
    if request.method == 'POST':
        id = request.POST['id']
        replies = Reply.objects.filter(article_id=id).annotate(
            custom_order=Case(
                When(reply_id=0, then='id'),
                default='reply_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')

        article = get_object_or_404(Board, pk=id)

        return render_to_response(
            'boards/show_reply.html',
            {
                'user': request.user,
                'article_user': article.user,
                'replies': replies,
                'count': replies.count()
            }
        )
    else:
        return error_page(request)


def delete_reply(request):
    """API delete_reply"""
    if request.method == 'POST':
        id = request.POST['id']
        reply = get_object_or_404(Reply, pk=id)

        if request.user == reply.user or request.user.is_staff:
            reply.status = '6deleted'
            reply.save()

            article_id = reply.article_id
            replies = Reply.objects.filter(article_id=article_id).annotate(
                custom_order=Case(
                    When(reply_id=0, then='id'),
                    default='reply_id',
                    output_field=IntegerField(),
                )
            ).order_by('custom_order', 'id')

            article = get_object_or_404(Board, pk=article_id)

            return render_to_response(
                'boards/show_reply.html',
                {
                    'user': request.user,
                    'article_user': article.user,
                    'replies': replies,
                    'count': replies.count()
                }
            )

    return error_page(request)


def reply_count(request):
    """API reply_count"""
    if request.method == 'POST':
        id = request.POST['id']
        article = get_object_or_404(Board, pk=id)
        count = article.reply_count

        return JsonResponse([count], safe=False, status=201)

    return error_page(request)


def toggle_bookmark(request):
    """API toggle_bookmark"""
    if request.method == 'POST':
        app = request.POST['app']
        id = request.POST['id']
        app_id = app + ':' + id
        profile = request.user.profile
        bookmarks = profile.bookmarks.split(',')

        if app_id not in bookmarks:
            if profile.bookmarks != '':
                profile.bookmarks += ","
            profile.bookmarks += app_id
            data = static('icons/stared28.png')
        else:
            regstr = re.escape(app_id) + r"\b(,|)"
            profile.bookmarks = re.sub(regstr, '', profile.bookmarks)
            if profile.bookmarks and profile.bookmarks[-1] == ',':
                profile.bookmarks = profile.bookmarks[:-1]
            data = static('icons/star28.png')

        request.user.profile.save()
        return JsonResponse([data], safe=False, status=201)

    return error_page(request)


def scrap(request):
    """API scrap"""
    if request.method == 'POST':
        app = request.POST['app']
        id = request.POST['id']
        app_id = app + ':' + id
        profile = request.user.profile
        scrap = profile.scrap.split(',')

        if app_id not in scrap:
            if profile.scrap != '':
                profile.scrap += ","
            profile.scrap += app_id

            request.user.profile.save()
            return JsonResponse({'status': 'true'}, status=201)
        else:
            return JsonResponse({'status': 'false'}, status=400)

    return error_page(request)


def alarm_status(request):
    """API alarm_status"""
    if request.user.is_authenticated():
        return JsonResponse([request.user.profile.alarm], safe=False, status=201)

    return JsonResponse({'status': 'false'}, status=400)


def alarm_list(request):
    """API alarm_list"""
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        type = request.POST['type']
        alarms = request.user.profile.alarm_list.split(',')
        my_alarms = []
        board_table = BoardTable()
        name_list = board_table.get_table_list()

        if request.user.profile.alarm_list != '':
            total = len(alarms)
            for alarm in reversed(alarms):
                app, id = alarm.split(':')
                if app == 'b':
                    item = Board.objects.filter(id__iexact=id)
                elif app == 'r':
                    item = Reply.objects.filter(id__iexact=id)
                else:
                    continue

                if item.count():
                    my_alarms.append([app, item[0]])

            if request.user.profile.alarm:
                request.user.profile.alarm = False
                request.user.profile.save()
        else:
            total = 0

        return render_to_response(
            'accounts/alarm_list.html',
            {
                'user': request.user,
                'alarms': my_alarms,
                'total': total,
                'max': settings.ALARM_INBOX_MAX,
                'type': type,
                'name_list': name_list,
            }
        )
    else:
        return error_page(request)

    return JsonResponse({'status': 'false'}, status=400)


def clear_alarm(request):
    """API clear_alarm"""
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        request.user.profile.alarm_list = ''
        request.user.profile.save()

        return JsonResponse({'status': 'true'}, status=201)
    else:
        return JsonResponse({'status': 'false'}, status=400)
