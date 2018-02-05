# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from boards.models import Board
from boards.table import BoardTable

from django.db.models import Q
from django.shortcuts import redirect, render


def portal(request, page=''):
    """Redirect to blog"""
    # redirect example
    if page == '1019':
        return redirect('blogs:show_post', id=43)
    elif page == '1039':
        return redirect('blogs:show_post', id=44)
    elif page == '1044':
        return redirect('blogs:show_post', id=45)
    elif page == '1064':
        return redirect('blogs:show_post', id=46)
    elif page == '1080':
        return redirect('blogs:show_post', id=47)
    elif page == '1318':
        return redirect('blogs:show_post', id=48)
    elif page == '1364':
        return redirect('blogs:show_post', id=50)
    elif page == '1374':
        return redirect('blogs:show_post', id=52)
    elif page == '1168':
        return redirect('blogs:show_post', id=53)
    elif page == '1260':
        return redirect('blogs:show_post', id=54)
    # end of example

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
