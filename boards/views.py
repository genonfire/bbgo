# -*- coding: utf-8 -*-
from math import ceil

from core.utils import error_page, get_ipaddress

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _

from models import Board, Reply

from .forms import BoardEditForm
from .table import BoardTable


def show_list(request, search_type='', search_word='', table=0, page=0):
    """Show list"""
    board_table = BoardTable()
    if int(table) >= board_table.get_table_len():
        return error_page(request)

    table_name = board_table.get_table_name(table)
    if table_name == '':
        return error_page(request)

    if int(page) < 1:
        return redirect('boards:show_list', table=table, page=1)

    table_desc = board_table.get_table_desc(table)
    list_count = board_table.get_list_count()

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    sq = (Q(status='1normal') | Q(status='4warning') | Q(status='5hidden'))
    if search_type == 'subject':
        q = sq & Q(subject__icontains=search_word)
    elif search_type == 'subjectcontent':
        q = sq & (
            Q(subject__icontains=search_word) |
            Q(content__icontains=search_word))
    elif search_type == 'writeuser':
        q = sq & (
            Q(user__username__icontains=search_word) |
            Q(user__first_name__icontains=search_word))
    else:
        q = sq

    if int(table) == 0 or int(table) == 9:
        if search_type == '':
            notice_list = Board.objects.filter(table=1).filter(
                status='3notice').order_by('-id')
        else:
            notice_list = None
        if int(table) == 9:
            total = Board.objects.filter(q).filter(
                like_count__gte=board_table.get_best_threshold()).filter(
                dislike_count__lte=board_table.get_veto_threshold()).count()
            lists = Board.objects.filter(q).filter(
                like_count__gte=board_table.get_best_threshold()).filter(
                dislike_count__lt=board_table.get_veto_threshold()) \
                .order_by('-id')[start_at:end_at]
        else:
            total = Board.objects.filter(q).count()
            lists = Board.objects.filter(q).order_by('-id')[start_at:end_at]
        name_list = board_table.get_table_list()
    else:
        if search_type == '':
            notice_list = Board.objects.filter(Q(table=1) | Q(table=table)).filter(status__iexact='3notice').order_by('table', '-id')
        else:
            notice_list = None
        total = Board.objects.filter(table=table).filter(q).count()
        lists = Board.objects.filter(table=table).filter(q).order_by('-id')[start_at:end_at]
        name_list = None

    index_total = int(ceil(float(total) / list_count))
    index_begin = (current_page / 10) * 10 + 1
    index_end = mindex_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9
    mindex_begin = (current_page / 5) * 5 + 1
    if mindex_end - mindex_begin >= 5:
        mindex_end = mindex_begin + 4

    writable = board_table.writable(request, table)

    return render(
        request,
        "boards/show_list.html",
        {
            'notice_list': notice_list,
            'lists': lists,
            'total': total,
            'table': table,
            'table_name': table_name,
            'table_desc': table_desc,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'mindex_begin': mindex_begin,
            'mindex_end': mindex_end + 1,
            'index_total': index_total,
            'writable': writable,
            'name_list': name_list,
            'search_type': search_type,
            'search_word': search_word,
        }
    )


def show_article(request, id, table=-1):
    """Show article"""
    article = get_object_or_404(Board, pk=id)

    if article.status == '5hidden' and not request.user.is_staff:
        errormsg = _('status_hidden')
        return error_page(request, errormsg)
    elif article.status == '6deleted' and not request.user.is_staff:
        errormsg = _('status_deleted')
        return error_page(request, errormsg)
    elif article.status == '2temp' and not request.user == article.user:
        return error_page(request)

    article.view_count += 1
    article.save()

    if int(table) == -1:
        table = article.table
    board_table = BoardTable()
    table_name = board_table.get_table_name(table)
    table_desc = board_table.get_table_desc(table)

    if article.status != '1normal':
        status_text = article.get_status_text()
    else:
        status_text = ''

    return render(
        request,
        "boards/show_article.html",
        {
            'article': article,
            'table': table,
            'table_name': table_name,
            'table_desc': table_desc,
            'status_text': status_text,
        }
    )


@login_required
def new_article(request, table=0):
    """New article"""
    if int(table) == 0 or (int(table) < 10 and not request.user.is_staff):
        return error_page(request)

    if request.method == "POST":
        editform = BoardEditForm(request.POST, request.FILES)
        if editform.is_valid():
            article = editform.save(commit=False)
            if article.status != '1normal' and article.status != '2temp':
                if not request.user.is_staff:
                    errormsg = _("Wrong status from user.")
                    return error_page(request, errormsg)
            article.user = request.user
            article.ip = get_ipaddress(request)
            article.table = table
            article.save()

            request.user.profile.last_article_at = timezone.now()
            request.user.profile.save()

            return redirect(article.get_absolute_url())
    elif request.method == "GET":
        editform = BoardEditForm()

    board_table = BoardTable()
    if int(table) >= board_table.get_table_len():
        return error_page(request)

    table_name = board_table.get_table_name(table)
    if table_name == '':
        return error_page(request)

    table_desc = board_table.get_table_desc(table)
    category_choices = board_table.get_category(table)

    return render(
        request,
        'boards/edit_article.html',
        {
            'form': editform,
            'edit_type': 'new',
            'table_name': table_name,
            'table_desc': table_desc,
            'category_choices': category_choices,
        }
    )


@login_required
def edit_article(request, id):
    """Edit article"""
    article = get_object_or_404(Board, pk=id)

    if request.method == "POST":
        editform = BoardEditForm(request.POST, request.FILES, instance=article)
        if editform.is_valid():
            article = editform.save(commit=False)
            article.modified_at = timezone.now()
            article.save()

            request.user.profile.last_article_at = timezone.now()
            request.user.profile.save()

            return redirect(article.get_article_url())
    elif request.method == "GET":
        board_table = BoardTable()
        if article.table >= board_table.get_table_len():
            return error_page(request)

        table_name = board_table.get_table_name(article.table)
        if table_name == '':
            return error_page(request)

        table_desc = board_table.get_table_desc(article.table)
        category_choices = board_table.get_category(article.table)

        editform = BoardEditForm(instance=article)

    return render(
        request,
        'boards/edit_article.html',
        {
            'form': editform,
            'edit_type': 'edit',
            'table_name': table_name,
            'table_desc': table_desc,
            'category_choices': category_choices,
        }
    )


@login_required
def delete_article(request, id):
    """Delete article"""
    article = get_object_or_404(Board, pk=id)

    if request.user == article.user:
        article.status = '6deleted'
        article.save()
    elif request.user.is_staff:
        article.status = '5hidden'
        article.save()
    else:
        return error_page(request)

    return redirect(article.get_absolute_url())


def search_article(request, search_type, search_word, table=0):
    """Search article"""
    return redirect(reverse_lazy('boards:show_search_article', kwargs={
        'search_type': search_type, 'search_word': search_word, 'table': table, 'page': 1}))


def search_reply(request, search_type, search_word, table=0, page=1):
    """Show reply list"""
    board_table = BoardTable()
    if int(table) >= board_table.get_table_len():
        return error_page(request)

    table_name = board_table.get_table_name(table)
    if table_name == '':
        return error_page(request)

    list_count = board_table.get_list_count()

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    if search_type == 'writeuser':
        q = Q(status__iexact='1normal') & (
            Q(user__username__iexact=search_word) |
            Q(user__first_name__iexact=search_word))
    else:
        return error_page(request)

    total = Reply.objects.filter(q).count()
    lists = Reply.objects.filter(q).order_by('-id')[start_at:end_at]
    name_list = board_table.get_table_list()

    index_total = int(ceil(float(total) / list_count))
    index_begin = (current_page / 10) * 10 + 1
    index_end = mindex_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9
    mindex_begin = (current_page / 5) * 5 + 1
    if mindex_end - mindex_begin >= 5:
        mindex_end = mindex_begin + 4

    return render(
        request,
        "boards/search_reply.html",
        {
            'lists': lists,
            'total': total,
            'table': table,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'mindex_begin': mindex_begin,
            'mindex_end': mindex_end + 1,
            'index_total': index_total,
            'name_list': name_list,
            'search_type': search_type,
            'search_word': search_word,
        }
    )


@login_required
def delete_reply(request, id):
    """Delete reply"""
    reply = get_object_or_404(Reply, pk=id)
    if request.user == reply.user:
        reply.status = '6deleted'
    elif request.user.is_staff:
        reply.status = '5hidden'
    else:
        return error_page(request)

    reply.save()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)
