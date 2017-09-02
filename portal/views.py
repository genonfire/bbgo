# -*- coding: utf-8 -*-
from random import randint

from boards.models import Board
from boards.table import BoardTable

from django.db.models import Q
from django.shortcuts import render

from teams.models import Team


def portal(request):
    """Portal"""
    banner_limit = 4
    banner = randint(0, banner_limit)

    board_table = BoardTable()
    sample_limit, sample_limit_mobile = board_table.get_sample_limit()
    sample_notice = board_table.get_sample_notice()

    q = Q(like_count__gte=board_table.get_best_threshold()) & Q(
        dislike_count__lt=board_table.get_veto_threshold())
    qs = Q(status='1normal') | Q(status='3notice') | Q(status='4warning')
    best = Board.objects.filter(q).filter(qs).order_by('-id')[0:sample_limit]
    notice = Board.objects.filter(qs).filter(table=2).order_by('-id')[
        0:sample_notice]
    info = Board.objects.filter(qs).filter(table=11).order_by('-id')[
        0:sample_limit]
    ps4 = Team.objects.filter(qs).filter(table=1).order_by('-id')[
        0:sample_limit]
    # pc = Team.objects.filter(qs).filter(table=3).order_by('-id')[
    #     0:sample_limit]

    return render(
        request,
        "portal/index.html",
        {
            'banner': banner,
            'best': best,
            'info': info,
            'notice': notice,
            'ps4': ps4,
            # 'pc': pc,
            'sample_limit_mobile': sample_limit_mobile,
        }
    )
