# -*- coding: utf-8 -*-
import sys

from boards.models import Board

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

reload(sys)
sys.setdefaultencoding('utf-8')


def like_article(request, liketype):
    """API like article"""
    if not request.user.is_authenticated():
        msg = _("require login")
        return JsonResponse([0, msg], safe=False, status=201)

    if request.method == 'POST':
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
    """API like users"""
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
