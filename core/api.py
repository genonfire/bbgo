# -*- coding: utf-8 -*-
from boards.forms import ReplyEditForm
from boards.models import Board, Reply
from core.utils import get_ipaddress

from django.contrib.auth.models import User
from django.db.models import Case, IntegerField, When
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone
from django.utils.translation import ugettext as _


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
        msg = _("Wrong access")
        return HttpResponse(msg)


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
        msg = _("Wrong access")
        return HttpResponse(msg)


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
        msg = _("Wrong access")
        return HttpResponse(msg)


def write_reply(request):
    """API write_reply"""
    if not request.user.is_authenticated():
        return JsonResponse({'status': 'false'}, status=400)

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
                alarm_text = 'a.%d' % article.id
                article.user.profile.alarm_list += alarm_text
                article.user.profile.alarm = True
                article.user.profile.save()
            elif reply_to != request.user.username and reply_id > 0:
                user = User.objects.filter(username=reply_to)
                if user:
                    print user[0].username
                    if user[0].profile.alarm_list != '':
                        user[0].profile.alarm_list += ','
                    alarm_text = 'r.%d' % reply_id
                    user[0].profile.alarm_list += alarm_text
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
                    'replies': replies,
                    'count': replies.count()
                }
            )

        return JsonResponse({'status': 'false'}, status=400)
    else:
        msg = _("Wrong access")
        return HttpResponse(msg)


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

        return render_to_response(
            'boards/show_reply.html',
            {
                'user': request.user,
                'replies': replies,
                'count': replies.count()
            }
        )
    else:
        msg = _("Wrong access")
        return HttpResponse(msg)


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

            return render_to_response(
                'boards/show_reply.html',
                {
                    'user': request.user,
                    'replies': replies,
                    'count': replies.count()
                }
            )

    msg = _("Wrong access")
    return HttpResponse(msg)


def alarm_off(request):
    """API alarm_off"""
    if request.user.is_authenticated():
        request.user.profile.alarm = False
        request.user.profile.save()

        return HttpResponse(status=204)
