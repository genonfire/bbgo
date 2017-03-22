#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from models import Board
from board.forms import BoardEditForm

from bbgo.utils import *
from django.conf import settings

from math import ceil

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def show_list(request, table=0, page=0):
    if int(page) < 1:
        return redirect('board show page', table=table, page=1)

    current_page = int(page) - 1
    start_at = current_page * int(settings.BOARD_LIST_COUNT)
    end_at = start_at + int(settings.BOARD_LIST_COUNT)
    lists = Board.objects.filter(table=table).order_by('-id')[start_at:end_at]
    total = Board.objects.filter(table=table).count()
    now = timezone.now()

    index_begin = (current_page / 10) * 10 + 1
    index_total = int(ceil(float(total) / settings.BOARD_LIST_COUNT))
    index_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9

    return render(
        request,
        "showboardlist.html",
        {
            'lists' : lists,
            'total' : total,
            'today' : now.date,
            'page' : current_page + 1,
            'index_begin' : index_begin,
            'index_end' : index_end + 1,
            'index_total' : index_total,
            'prev_index' : index_begin - 1,
            'next_index' : index_end + 1,
        }
    )

@login_required
def new_article(request, table=0,):
    if request.method == "POST":
        editform = BoardEditForm(request.POST, request.FILES)
        if editform.is_valid():
            article = editform.save(commit=False)
            article.user = request.user
            article.ip = get_ipaddress(request)
            article.table = table
            article.save()

            return redirect(article.get_absolute_url())
    elif request.method == "GET":
        editform = BoardEditForm()

    return render(
        request,
        'editboard.html',
        {
            'form': editform,
            'editType': 'new',
        }
    )

