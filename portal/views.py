# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from boards.models import Board
from boards.table import BoardTable

from django.db.models import Q
from django.shortcuts import redirect, render


def portal(request, page=''):
    """Redirect"""
    if page:
        return redirect('boards:show_article', id=page)

    return redirect('blogs:blog_home')


def bbgo(request):
    """Show board samples"""
    board_table = BoardTable()
    sample_limit, sample_limit_mobile = board_table.get_sample_limit()

    qs = Q(status='1normal') | Q(status='3notice') | Q(status='4warning')
    table = Q(table=3) | Q(table=12)
    bbs = Board.objects.filter(qs).filter(table).order_by('-id')[
        0:sample_limit]

    return render(
        request,
        "portal/bbgo.html",
        {
            'bbs': bbs,
            'sample_limit_mobile': sample_limit_mobile,
            'app': 'bbgo',
        }
    )
