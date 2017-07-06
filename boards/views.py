# -*- coding: utf-8 -*-
from math import ceil
import sys

from core.utils import get_ipaddress, get_template

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from models import Board

from .forms import BoardEditForm
from .table import BoardTable
reload(sys)
sys.setdefaultencoding('utf-8')


def show_list(request, table=0, page=0):
    """Show list"""
    board_table = BoardTable()
    if int(table) >= board_table.get_table_len():
        return HttpResponse(u"잘못된 접근입니다.")

    table_name = board_table.get_table_name(table)
    if table_name == '':
        return HttpResponse(u"잘못된 접근입니다.")

    if int(page) < 1:
        return redirect('boards:show_list', table=table, page=1)

    board_desc = board_table.get_table_desc(table)
    list_count = board_table.get_list_count()

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    if int(table) == 0:
        total = Board.objects.filter().count()
        lists = Board.objects.filter().order_by('-id')[start_at:end_at]
    else:
        total = Board.objects.filter(table=table).count()
        lists = Board.objects.filter(table=table).order_by('-id')[start_at:end_at]
    now = timezone.now()

    index_begin = (current_page / 10) * 10 + 1
    index_total = int(ceil(float(total) / list_count))
    index_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9

    check_write = True
    if int(table) == 0 or (int(table) < 10 and not request.user.is_staff):
        check_write = False

    return render(
        request,
        get_template(request, "boards/m-show_list.html"),
        {
            'lists': lists,
            'total': total,
            'today': now.date,
            'table': table,
            'table_name': table_name,
            'board_desc': board_desc,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'index_total': index_total,
            'prev_index': index_begin - 1,
            'next_index': index_end + 1,
            'check_write': check_write,
        }
    )


def show_article(request, id):
    """Show article"""
    article = get_object_or_404(Board, pk=id)
    article.view_count += 1
    article.save()

    return render(
        request,
        "boards/show_article.html",
        {
            'article': article,
        }
    )


@login_required
def new_article(request, table=0):
    """New article"""
    if int(table) == 0 or (int(table) < 10 and not request.user.is_staff):
        return HttpResponse(u"잘못된 접근입니다.")

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
        board_table = BoardTable()
        if int(table) >= board_table.get_table_len():
            return HttpResponse(u"잘못된 접근입니다.")

        table_name = board_table.get_table_name(table)
        if table_name == '':
            return HttpResponse(u"잘못된 접근입니다.")

        board_desc = board_table.get_table_desc(table)
        category_choices = board_table.get_category(table)

        editform = BoardEditForm()

        return render(
            request,
            'boards/edit_article.html',
            {
                'form': editform,
                'editType': 'new',
                'table_name': table_name,
                'board_desc': board_desc,
                'category_choices': category_choices,
                'is_staff': request.user.is_staff,
            }
        )
