# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from smtplib import SMTPException
import threading

from blogs.forms import CommentEditForm
from blogs.models import Blog, Comment
from boards.forms import ReplyEditForm
from boards.models import Board, Reply
from boards.table import BoardTable
from core.utils import error_page, error_to_response, get_ipaddress

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.db.models import Case, IntegerField, Q, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone
from django.utils.translation import ugettext as _

from msgs.models import Msg
from papers.models import Paper, Person
from papers.views import send_email_with_paper
from spams.views import check_spam
from teams.forms import TeamReplyEditForm
from teams.models import Team, TeamReply


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

    if request.user.is_authenticated and idcheck:
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
        if not request.user.is_authenticated:
            msg = _("Require login")
            return JsonResponse([0, msg], safe=False, status=201)

        id = request.POST['id']
        user = request.user
        article = get_object_or_404(Board, pk=id)

        if article.user == user:
            msg = _("You like your own post?")
            return JsonResponse([0, msg], safe=False, status=201)

        like_users = article.like_users.all()
        dislike_users = article.dislike_users.all()

        if user not in like_users and user not in dislike_users:
            if liketype == 'like':
                article.like_users.add(user)
                article.like_count += 1
                article.save()

                msg = _("You've liked this article")
                return JsonResponse(
                    [article.like_count, msg], safe=False, status=201)
            elif liketype == 'dislike':
                article.dislike_users.add(user)
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
            like_users = article.like_users.all()
        elif liketype == 'dislike':
            like_users = article.dislike_users.all()
        else:
            return JsonResponse({'status': 'false'}, status=400)

        return render_to_response(
            'boards/like_users.html',
            {
                'user': request.user,
                'like_users': like_users,
            }
        )

    else:
        return error_page(request)


def like_reply(request, liketype):
    """API like_reply"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            msg = _("Require login")
            return JsonResponse([0, msg], safe=False, status=201)

        id = request.POST['id']
        user = request.user
        reply = get_object_or_404(Reply, pk=id)

        if reply.user == user:
            msg = _("You like your own post?")
            return JsonResponse([0, msg], safe=False, status=201)

        like_users = reply.like_users.all()
        dislike_users = reply.dislike_users.all()

        if user not in like_users and user not in dislike_users:
            if liketype == 'like':
                reply.like_users.add(user)
                reply.like_count += 1
                reply.save()

                return JsonResponse([reply.like_count], safe=False, status=201)
            elif liketype == 'dislike':
                reply.dislike_users.add(user)
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
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        id = request.POST['article_id']
        reply_id = r_id = int(request.POST['reply_id'])
        reply_to = ''

        form = ReplyEditForm(request.POST, request.FILES)
        if form.is_valid():
            article = get_object_or_404(Board, pk=id)
            if article.status != '1normal' and article.status != '3notice' \
                    and not request.user.is_staff:
                return JsonResponse({'status': 'false'}, status=402)

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

            article.reply_count += 1
            article.save()

            if article.user != request.user and reply_id == 0:
                if article.user.profile.alarm_board:
                    if article.user.profile.alarm_list != '':
                        article.user.profile.alarm_list += ','
                    alarm_text = 'b:%d' % article.id
                    article.user.profile.alarm_list += alarm_text
                    article.user.profile.alarm = True
                    article.user.profile.save()
            elif reply_to != request.user.username and reply_id > 0:
                user = User.objects.filter(username=reply_to)
                if user:
                    if user[0].profile.alarm_reply:
                        if user[0].profile.alarm_list != '':
                            user[0].profile.alarm_list += ','
                        alarm_text = 'r:%d' % r_id
                        user[0].profile.alarm_list += alarm_text
                        user[0].profile.alarm = True
                        user[0].save()

            request.user.profile.last_reply_at = timezone.now()
            request.user.profile.point += settings.POINT_REPLY
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
        return error_to_response(request)


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
        return error_to_response(request)


def delete_reply(request, early_return=False):
    """API delete_reply"""
    if request.method == 'POST':
        id = request.POST['id']
        reply = get_object_or_404(Reply, pk=id)

        if request.user == reply.user:
            reply.status = '6deleted'
        elif request.user.is_staff:
            reply.status = '5hidden'
        else:
            return error_to_response(request)

        reply.save()
        if early_return:
            return JsonResponse({'status': 'true'}, status=201)

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

    return error_to_response(request)


def restore_reply(request):
    """API restore_reply"""
    if request.method == 'POST':
        id = request.POST['id']
        reply = get_object_or_404(Reply, pk=id)

        if request.user.is_staff:
            reply.status = '1normal'
        else:
            return error_to_response(request)

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

    return error_to_response(request)


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
        app_id = app + '-' + id
        profile = request.user.profile
        bookmarks = profile.bookmarks.split(',')

        if app_id not in bookmarks:
            if len(bookmarks) > settings.MAX_BOOKMARKS:
                return JsonResponse({'status': 'false'}, status=400)

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


def edit_bookmarks(request):
    """API edit_bookmarks"""
    if request.method == 'POST':
        bookmarks = dict(request.POST.iterlists())['bookmarks[]']
        my_bookmarks = ''

        for bm in bookmarks:
            if my_bookmarks != '':
                my_bookmarks += ","
            my_bookmarks += bm
        request.user.profile.bookmarks = my_bookmarks
        request.user.profile.save()

        return JsonResponse({'status': 'true'}, status=201)

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
    if request.user.is_authenticated:
        return JsonResponse([request.user.profile.alarm], safe=False, status=201)

    return JsonResponse({'status': 'false'}, status=400)


def alarm_list(request):
    """API alarm_list"""
    if not request.user.is_authenticated:
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
                elif app == 'l':
                    item = Blog.objects.filter(id__iexact=id)
                elif app == 'c':
                    item = Comment.objects.filter(id__iexact=id)
                elif app == 'pa' or app == 'pc' or app == 'pr':
                    item = Paper.objects.filter(id__iexact=id)
                elif app == 't' or app == 'tf' or app == 'tc' or app == 'tl' \
                        or app == 'tk' or app == 'bt':
                    item = Team.objects.filter(id__iexact=id)
                elif app == 'rt':
                    item = TeamReply.objects.filter(id__iexact=id)
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
        return error_to_response(request)

    return JsonResponse({'status': 'false'}, status=400)


def clear_alarm(request):
    """API clear_alarm"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        request.user.profile.alarm_list = ''
        request.user.profile.save()

        return JsonResponse({'status': 'true'}, status=201)
    else:
        return JsonResponse({'status': 'false'}, status=400)


def delete_message(request):
    """API delete_message"""
    if request.method == 'POST':
        id = request.POST['id']
        msg = get_object_or_404(Msg, pk=id)

        if msg.sender == request.user:
            msg.sender_status = '6deleted'
            msg.save()
        elif msg.recipient == request.user:
            msg.recipient_status = '6deleted'
            msg.save()
        else:
            return JsonResponse({'status': 'false'}, status=400)

        return JsonResponse({'status': 'true'}, status=201)

    return error_page(request)


def write_team_reply(request):
    """API write_team_reply"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        id = request.POST['article_id']
        reply_id = rt_id = int(request.POST['reply_id'])
        reply_to = ''

        form = TeamReplyEditForm(request.POST)
        if form.is_valid():
            article = get_object_or_404(Team, pk=id)
            if (article.status == '5hidden' or article.status == '6deleted') \
                    and not request.user.is_staff:
                return JsonResponse({'status': 'false'}, status=402)
            reply = form.save(commit=False)
            parent_id = reply_id

            while parent_id != 0:
                parent = get_object_or_404(TeamReply, pk=parent_id)
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

            article.reply_count += 1
            article.save()

            if article.user != request.user and reply_id == 0:
                if article.user.profile.alarm_board:
                    if article.user.profile.alarm_list != '':
                        article.user.profile.alarm_list += ','
                    alarm_text = 'bt:%d' % article.id
                    article.user.profile.alarm_list += alarm_text
                    article.user.profile.alarm = True
                    article.user.profile.save()
            elif reply_to != request.user.username and reply_id > 0:
                user = User.objects.filter(username=reply_to)
                if user:
                    if user[0].profile.alarm_reply:
                        if user[0].profile.alarm_list != '':
                            user[0].profile.alarm_list += ','
                        alarm_text = 'rt:%d' % rt_id
                        user[0].profile.alarm_list += alarm_text
                        user[0].profile.alarm = True
                        user[0].save()

            request.user.profile.last_reply_at = timezone.now()
            request.user.profile.point += settings.POINT_REPLY
            request.user.profile.save()

            replies = TeamReply.objects.filter(article_id=id).annotate(
                custom_order=Case(
                    When(reply_id=0, then='id'),
                    default='reply_id',
                    output_field=IntegerField(),
                )
            ).order_by('custom_order', 'id')

            return render_to_response(
                'teams/show_team_reply.html',
                {
                    'user': request.user,
                    'article_user': article.user,
                    'replies': replies,
                    'count': replies.count()
                }
            )

        return JsonResponse({'status': 'false'}, status=400)
    else:
        return error_to_response(request)


def reload_team_reply(request):
    """API reload_team_reply"""
    if request.method == 'POST':
        id = request.POST['id']
        replies = TeamReply.objects.filter(article_id=id).annotate(
            custom_order=Case(
                When(reply_id=0, then='id'),
                default='reply_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')

        article = get_object_or_404(Team, pk=id)

        return render_to_response(
            'teams/show_team_reply.html',
            {
                'user': request.user,
                'article_user': article.user,
                'replies': replies,
                'count': replies.count()
            }
        )
    else:
        return error_to_response(request)


def delete_team_reply(request):
    """API delete_team_reply"""
    if request.method == 'POST':
        id = request.POST['id']
        reply = get_object_or_404(TeamReply, pk=id)

        if request.user == reply.user:
            reply.status = '6deleted'
        elif request.user.is_staff:
            reply.status = '5hidden'
        else:
            return error_to_response(request)

        reply.save()
        article_id = reply.article_id
        replies = TeamReply.objects.filter(article_id=article_id).annotate(
            custom_order=Case(
                When(reply_id=0, then='id'),
                default='reply_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')

        article = get_object_or_404(Team, pk=article_id)

        return render_to_response(
            'teams/show_team_reply.html',
            {
                'user': request.user,
                'article_user': article.user,
                'replies': replies,
                'count': replies.count()
            }
        )

    return error_to_response(request)


def restore_team_reply(request):
    """API restore_team_reply"""
    if request.method == 'POST':
        id = request.POST['id']
        reply = get_object_or_404(TeamReply, pk=id)

        if request.user.is_staff:
            reply.status = '1normal'
        else:
            return error_to_response(request)

        reply.save()
        article_id = reply.article_id
        replies = TeamReply.objects.filter(article_id=article_id).annotate(
            custom_order=Case(
                When(reply_id=0, then='id'),
                default='reply_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')

        article = get_object_or_404(Team, pk=article_id)

        return render_to_response(
            'teams/show_team_reply.html',
            {
                'user': request.user,
                'article_user': article.user,
                'replies': replies,
                'count': replies.count()
            }
        )

    return error_to_response(request)


def team_reply_count(request):
    """API team_reply_count"""
    if request.method == 'POST':
        id = request.POST['id']
        article = get_object_or_404(Team, pk=id)
        count = article.reply_count
        slot = article.slot

        return JsonResponse([count, slot], safe=False, status=201)

    return error_page(request)


def join_team(request):
    """API join_team"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'false'}, status=401)

        id = request.POST['id']
        user = request.user
        article = get_object_or_404(Team, pk=id)

        if article.table == 1:
            if not user.profile.id1:
                return JsonResponse({'status': 'false'}, status=412)
        elif article.table == 2:
            if not user.profile.id2:
                return JsonResponse({'status': 'false'}, status=412)
        elif article.table == 3:
            if not user.profile.id3:
                return JsonResponse({'status': 'false'}, status=412)

        if article.user == user:
            return JsonResponse({'status': 'false'}, status=405)

        if article.slot >= article.slot_total:
            return JsonResponse({'status': 'false'}, status=406)

        if article.status == '1normal':
            slots = article.slot_users.all()

            if user not in slots:
                article.slot_users.add(user)
                article.slot += 1

                if article.slot == article.slot_total:
                    article.status = '8full'
                article.save()
                slot_users = article.slot_users.all()

                if article.user.profile.alarm_team or (
                    article.slot == article.slot_total and
                    article.user.profile.alarm_full
                ):
                    if article.user.profile.alarm_list != '':
                        article.user.profile.alarm_list += ','
                    if article.user.profile.alarm_full and \
                            article.slot == article.slot_total:
                        alarm_text = 'f:%d' % article.id
                    else:
                        alarm_text = 't:%d' % article.id
                    article.user.profile.alarm_list += alarm_text
                    article.user.profile.alarm = True
                    article.user.save()

                if article.slot == article.slot_total:
                    for slot_user in slot_users:
                        if slot_user.profile.alarm_full:
                            if slot_user.profile.alarm_list != '':
                                slot_user.profile.alarm_list += ','
                            alarm_text = 'f:%d' % article.id
                            slot_user.profile.alarm_list += alarm_text
                            slot_user.profile.alarm = True
                            slot_user.save()

                return render_to_response(
                    'teams/show_team.html',
                    {
                        'user': user,
                        'table': article.table,
                        'article_id': article.id,
                        'article_user': article.user,
                        'slot_in': article.slot,
                        'empty_slots': article.slot_total - article.slot,
                        'slot_users': slot_users,
                    }
                )
            else:
                return JsonResponse({'status': 'false'}, status=405)
        elif article.status == '7canceled':
            return JsonResponse({'status': 'false'}, status=410)
        elif article.status == '8full':
            return JsonResponse({'status': 'false'}, status=406)
        elif article.status == '5hidden' or article.status == '6deleted':
            return JsonResponse({'status': 'false'}, status=404)
        else:
            return JsonResponse({'status': 'false'}, status=400)
    else:
        return error_page(request)


def leave_team(request):
    """API leave_team"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'false'}, status=401)

        id = request.POST['id']
        user = request.user
        article = get_object_or_404(Team, pk=id)

        if article.user == user:
            return JsonResponse({'status': 'false'}, status=403)

        slots = article.slot_users.all()

        if user in slots:
            article.slot_users.remove(user)
            if article.slot > 1:
                article.slot -= 1

            if article.status == '8full':
                article.status = '1normal'
            article.save()
            slot_users = article.slot_users.all()

            if article.user.profile.alarm_team:
                if article.user.profile.alarm_list != '':
                    article.user.profile.alarm_list += ','
                alarm_text = 'l:%d' % article.id
                article.user.profile.alarm_list += alarm_text
                article.user.profile.alarm = True
                article.user.save()

            return render_to_response(
                'teams/show_team.html',
                {
                    'user': user,
                    'table': article.table,
                    'article_id': article.id,
                    'article_user': article.user,
                    'slot_in': article.slot,
                    'empty_slots': article.slot_total - article.slot,
                    'slot_users': slot_users,
                }
            )
        else:
            return JsonResponse({'status': 'false'}, status=404)
    else:
        return error_page(request)


def kick_player(request):
    """API reload_team"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'false'}, status=401)

        id = request.POST['id']
        kick = request.POST['kick_user']
        kick_user = User.objects.filter(username__iexact=kick).get()
        user = request.user
        article = get_object_or_404(Team, pk=id)

        if article.user != user and not user.is_staff:
            return JsonResponse({'status': 'false'}, status=403)

        slots = article.slot_users.all()

        if kick_user in slots:
            article.slot_users.remove(kick_user)
            if article.slot > 1:
                article.slot -= 1

            if article.status == '8full':
                article.status = '1normal'
            article.save()
            slot_users = article.slot_users.all()

            if article.user.profile.alarm_team:
                if article.user.profile.alarm_list != '':
                    article.user.profile.alarm_list += ','
                alarm_text = 'l:%d' % article.id
                article.user.profile.alarm_list += alarm_text
                article.user.profile.alarm = True
                article.user.save()

            if kick_user.profile.alarm_list != '':
                kick_user.profile.alarm_list += ','
            alarm_text = 'k:%d' % article.id
            kick_user.profile.alarm_list += alarm_text
            kick_user.profile.alarm = True
            kick_user.save()

            return render_to_response(
                'teams/show_team.html',
                {
                    'user': user,
                    'table': article.table,
                    'article_id': article.id,
                    'article_user': article.user,
                    'slot_in': article.slot,
                    'empty_slots': article.slot_total - article.slot,
                    'slot_users': slot_users,
                }
            )
        else:
            return JsonResponse({'status': 'false'}, status=404)
    else:
        return error_page(request)


def reload_team(request):
    """API reload_team"""
    if request.method == 'POST':
        id = request.POST['id']
        article = get_object_or_404(Team, pk=id)
        slot_users = article.slot_users.all()

        return render_to_response(
            'teams/show_team.html',
            {
                'user': request.user,
                'table': article.table,
                'article_id': article.id,
                'article_user': article.user,
                'slot_in': article.slot,
                'empty_slots': article.slot_total - article.slot,
                'slot_users': slot_users,
            }
        )
    else:
        return error_to_response(request)


def like_post(request):
    """API like_post"""
    if request.method == 'POST':
        id = request.POST['id']
        ip = get_ipaddress(request)
        user = request.user
        post = get_object_or_404(Blog, pk=id)
        like_users = post.like_users.split(',')

        if post.user == user or ip == post.ip:
            msg = _("You like your own post?")
            return JsonResponse([0, msg], safe=False, status=201)

        if ip not in like_users:
            if post.like_users != '':
                post.like_users += ","
            post.like_users += ip
            post.like_count += 1
            post.save()

            msg = _("You've liked this article")
            return JsonResponse(
                [post.like_count, msg], safe=False, status=201)
        else:
            msg = _("You've already liked")
            return JsonResponse([0, msg], safe=False, status=201)
    else:
        return error_page(request)


def write_comment(request):
    """API write_comment"""
    if request.method == 'POST':
        id = request.POST['post_id']
        comment_id = r_id = int(request.POST['comment_id'])
        username = request.POST['username']

        form = CommentEditForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Blog, pk=id)
            if post.status != '1normal' and not request.user.is_staff:
                return JsonResponse({'status': 'false'}, status=402)

            comment = form.save(commit=False)
            parent_id = comment_id

            while parent_id != 0:
                parent = get_object_or_404(Comment, pk=parent_id)
                if parent:
                    parent_id = parent.comment_id
                    if parent_id == 0:
                        comment_id = parent.id
                else:
                    return JsonResponse({'status': 'false'}, status=400)

            comment.comment_id = comment_id
            comment.ip = get_ipaddress(request)
            comment.status = '1normal'
            if request.user.is_authenticated:
                comment.userid = request.user.username
            else:
                comment.username = username
                if check_spam(request, comment):
                    comment.status = '7spam'

            comment.save()

            post.comment_count += 1
            post.save()

            if comment.status != '7spam':
                if post.user != request.user and comment_id == 0:
                    if post.user.profile.alarm_list != '':
                        post.user.profile.alarm_list += ','
                    alarm_text = 'l:%d' % post.id
                    post.user.profile.alarm_list += alarm_text
                    post.user.profile.alarm = True
                    post.user.profile.save()
                elif comment_id > 0:
                    comment_to = get_object_or_404(Comment, pk=comment_id)
                    if comment_to and comment_to.userid:
                        user = User.objects.filter(username=comment_to.userid)
                        if user and user[0] is not request.user:
                            if user[0].profile.alarm_reply:
                                if user[0].profile.alarm_list != '':
                                    user[0].profile.alarm_list += ','
                                alarm_text = 'c:%d' % r_id
                                user[0].profile.alarm_list += alarm_text
                                user[0].profile.alarm = True
                                user[0].save()

            q = Q(status='1normal')
            comments = Comment.objects.filter(post_id=id).filter(q).annotate(
                custom_order=Case(
                    When(comment_id=0, then='id'),
                    default='comment_id',
                    output_field=IntegerField(),
                )
            ).order_by('custom_order', 'id')

            return render_to_response(
                'blogs/show_comment.html',
                {
                    'user': request.user,
                    'post_user': post.user.username,
                    'comments': comments,
                    'count': comments.count()
                }
            )

        return JsonResponse({'status': 'false'}, status=400)
    else:
        return error_to_response(request)


def delete_comment(request):
    """API delete_comment"""
    if request.method == 'POST':
        id = request.POST['id']
        comment = get_object_or_404(Comment, pk=id)

        if request.user.username == comment.userid or request.user.is_staff:
            comment.status = '6deleted'
        else:
            return error_to_response(request)

        comment.save()
        post_id = comment.post_id
        post = get_object_or_404(Blog, pk=post_id)
        post.comment_count -= 1
        post.save()

        q = Q(status='1normal')
        comments = Comment.objects.filter(post_id=post_id).filter(q).annotate(
            custom_order=Case(
                When(post_id=0, then='id'),
                default='post_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')

        return render_to_response(
            'blogs/show_comment.html',
            {
                'user': request.user,
                'post_user': post.user.username,
                'comments': comments,
                'count': comments.count()
            }
        )

    return error_to_response(request)


def reload_comment(request):
    """API reload_comment"""
    if request.method == 'POST':
        id = request.POST['id']
        post = get_object_or_404(Blog, pk=id)

        q = Q(status='1normal')
        comments = Comment.objects.filter(post_id=id).filter(q).annotate(
            custom_order=Case(
                When(post_id=0, then='id'),
                default='post_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')

        return render_to_response(
            'blogs/show_comment.html',
            {
                'user': request.user,
                'post_user': post.user.username,
                'comments': comments,
                'count': comments.count()
            }
        )
    else:
        return error_to_response(request)


def user_by_name(request):
    """API user_by_name"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        approval_type = request.POST['type']
        name = request.POST['name']
        blacklist = request.POST.getlist('blacklist[]')

        q = Q(username__icontains=name) | Q(
            first_name__icontains=name) | Q(last_name__icontains=name)

        names = User.objects.filter(is_active=True).filter(q).exclude(
            username__in=blacklist)
        total = names.count()

        if total == 1:
            data = {
                'type': approval_type,
                'id': names[0].id,
                'username': names[0].username,
                'name': names[0].last_name,
                'email': names[0].email,
                'status': 'only',
            }
            return JsonResponse(data)

        return render_to_response(
            'papers/user_list.html',
            {
                'user': request.user,
                'type': approval_type,
                'names': names,
                'total': total,
            }
        )
    else:
        return error_to_response(request)


def approve_paper(request):
    """API approve_paper"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        id = request.POST['id']
        comment = request.POST['comment']
        paper = get_object_or_404(Paper, pk=id)

        if paper.completed or request.user != paper.cc.last().user:
            return JsonResponse({'status': 'false'}, status=403)
        if paper.approved and request.user == paper.approver:
            return JsonResponse({'status': 'false'}, status=403)

        paper.updated_at = timezone.now()

        if request.user == paper.approver:
            paper.comment = comment
            paper.approved = True
            paper.approved_at = paper.updated_at

            if paper.supporters.all():
                paper.status = '2progress'
                first = paper.supporters.first()
                person = Person.objects.create(
                    order=first.order, user=first.user)
                paper.cc.add(person)
            else:
                paper.status = '5completed'
                paper.completed = True
                for notifier in paper.notifiers.all():
                    paper.cc.add(notifier)
        else:
            index = paper.cc.last().order - 3
            supporter = paper.supporters.all()[index]

            if index < 0 or supporter.user != request.user:
                return JsonResponse({'status': 'false'}, status=403)
            else:
                supporter.comment = comment
                supporter.approved = True
                supporter.approved_at = paper.updated_at
                supporter.save()

                if paper.supporters.last().user == request.user:
                    paper.status = '5completed'
                    paper.completed = True
                    for notifier in paper.notifiers.all():
                        paper.cc.add(notifier)
                else:
                    next_supporter = paper.supporters.all()[index + 1]
                    person = Person.objects.create(
                        order=next_supporter.order, user=next_supporter.user)
                    paper.cc.add(person)
        paper.save()

        if paper.status == '5completed':
            if paper.user.profile.alarm_paper:
                if paper.user.profile.alarm_list != '':
                    paper.user.profile.alarm_list += ','
                alarm_text = 'pc:%d' % paper.id
                paper.user.profile.alarm_list += alarm_text
                paper.user.profile.alarm = True
                paper.user.profile.save()
            if settings.PAPER_EMAIL_UPDATE:
                thread = threading.Thread(
                    target=send_email_with_paper, args=(request, id))
                thread.start()
        else:
            target = paper.cc.last().user
            if target.profile.alarm_paper:
                if target.profile.alarm_list != '':
                    target.profile.alarm_list += ','
                alarm_text = 'pa:%d' % paper.id
                target.profile.alarm_list += alarm_text
                target.profile.alarm = True
                target.profile.save()

        return JsonResponse({'status': 'true'}, status=201)


def reject_paper(request):
    """API reject_paper"""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false'}, status=401)

    if request.method == 'POST':
        id = request.POST['id']
        comment = request.POST['comment']
        paper = get_object_or_404(Paper, pk=id)

        if not paper.completed and request.user == paper.user:
            paper.updated_at = timezone.now()
            paper.cancelmsg = comment
            paper.status = '4canceled'
            paper.completed = True
            paper.save()
            return JsonResponse({'status': 'true'}, status=201)

        if paper.completed or request.user != paper.cc.last().user:
            return JsonResponse({'status': 'false'}, status=403)
        if paper.approved and request.user == paper.approver:
            return JsonResponse({'status': 'false'}, status=403)

        paper.updated_at = timezone.now()

        if request.user == paper.approver:
            paper.comment = comment
            paper.rejected = True
            paper.approved_at = paper.updated_at
        else:
            index = paper.cc.last().order - 3
            supporter = paper.supporters.all()[index]

            if index < 0 or supporter.user != request.user:
                return JsonResponse({'status': 'false'}, status=403)
            else:
                supporter.comment = comment
                supporter.rejected = True
                supporter.approved_at = paper.updated_at
                supporter.save()

        paper.status = '3rejected'
        paper.completed = True
        paper.save()

        if paper.user.profile.alarm_paper:
            if paper.user.profile.alarm_list != '':
                paper.user.profile.alarm_list += ','
            alarm_text = 'pr:%d' % paper.id
            paper.user.profile.alarm_list += alarm_text
            paper.user.profile.alarm = True
            paper.user.profile.save()
        if settings.PAPER_EMAIL_UPDATE:
            thread = threading.Thread(
                target=send_email_with_paper, args=(request, id))
            thread.start()

        return JsonResponse({'status': 'true'}, status=201)
