# -*- coding: utf-8 -*-
from random import randint

from boards.models import Board
from boards.table import BoardTable

from django.db.models import Q
from django.shortcuts import render


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
    recent = Board.objects.filter(qs).order_by('-id')[
        0:sample_notice]
    notice = Board.objects.filter(qs).filter(table=2).order_by('-id')[
        0:sample_notice]
    bbs = Board.objects.filter(qs).filter(table=12).order_by('-id')[
        0:sample_limit]

    return render(
        request,
        "portal/board_sample.html",
        {
            'banner': banner,
            'best': best,
            'recent': recent,
            'bbs': bbs,
            'notice': notice,
            'sample_limit_mobile': sample_limit_mobile,
        }
    )
