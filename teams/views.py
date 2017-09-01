# -*- coding: utf-8 -*-
from math import ceil

from core.utils import error_page, get_ipaddress

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _

from models import Team

from .forms import TeamEditForm
from .table import TeamTable


def recruitment(request, table=0, page=0):
    """Recruitment"""
    team_table = TeamTable()
    if int(table) >= team_table.get_table_len():
        return error_page(request)

    table_name = team_table.get_table_name(table)
    if table_name == '':
        return error_page(request)

    if int(page) < 1:
        return redirect('teams:recruitment', table=table, page=1)

    table_desc = team_table.get_table_desc(table)
    list_count = team_table.get_list_count()

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    q = Q(status='1normal') | Q(status='7canceled') | Q(status='8full')

    total = Team.objects.filter(table=table).filter(q).count()
    lists = Team.objects.filter(table=table).filter(q).order_by('-id')[start_at:end_at]

    index_total = int(ceil(float(total) / list_count))
    index_begin = (current_page / 10) * 10 + 1
    index_end = mindex_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9
    mindex_begin = (current_page / 5) * 5 + 1
    if mindex_end - mindex_begin >= 5:
        mindex_end = mindex_begin + 4

    if request.user.is_authenticated():
        writable = True
    else:
        writable = False

    return render(
        request,
        "teams/recruitment.html",
        {
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
        }
    )


def show_recruitment(request, id):
    """Show recruitment"""
    article = get_object_or_404(Team, pk=id)
    article.view_count += 1
    article.save()

    table = article.table
    team_table = TeamTable()
    table_name = team_table.get_table_name(table)
    table_desc = team_table.get_table_desc(table)

    if article.status != '1normal':
        status_text = article.get_status_text()
    else:
        status_text = ''

    return render(
        request,
        "teams/show_recruitment.html",
        {
            'article': article,
            'table': table,
            'table_name': table_name,
            'table_desc': table_desc,
            'status_text': status_text,
        }
    )


@login_required
def new_recruitment(request, table=0):
    """New recruitment"""
    if request.method == "POST":
        editform = TeamEditForm(request.POST)
        if editform.is_valid():
            print 'valid'
            article = editform.save(commit=False)
            if article.status != '1normal':
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
        else:
            print 'invalid'
    elif request.method == "GET":
        editform = TeamEditForm()

    team_table = TeamTable()
    if int(table) >= team_table.get_table_len():
        return error_page(request)

    table_name = team_table.get_table_name(table)
    if table_name == '':
        return error_page(request)

    table_desc = team_table.get_table_desc(table)
    category_choices = team_table.get_category(table)

    return render(
        request,
        'teams/edit_recruitment.html',
        {
            'form': editform,
            'edit_type': 'new',
            'table_name': table_name,
            'table_desc': table_desc,
            'category_choices': category_choices,
        }
    )


@login_required
def edit_recruitment(request, id):
    """Edit recruitment"""
    article = get_object_or_404(Team, pk=id)

    if request.method == "POST":
        editform = TeamEditForm(request.POST, instance=article)
        if editform.is_valid():
            article = editform.save(commit=False)
            article.modified_at = timezone.now()
            article.save()

            request.user.profile.last_article_at = timezone.now()
            request.user.profile.save()

            return redirect(article.get_article_url())
    elif request.method == "GET":
        team_table = TeamTable()
        if article.table >= team_table.get_table_len():
            return error_page(request)

        table_name = team_table.get_table_name(article.table)
        if table_name == '':
            return error_page(request)

        table_desc = team_table.get_table_desc(article.table)
        category_choices = team_table.get_category(article.table)

        editform = TeamEditForm(instance=article)

    return render(
        request,
        'teams/edit_recruitment.html',
        {
            'form': editform,
            'edit_type': 'edit',
            'table_name': table_name,
            'table_desc': table_desc,
            'category_choices': category_choices,
        }
    )


@login_required
def change_status(request, id, status):
    """Change status"""
    article = get_object_or_404(Team, pk=id)

    if request.user == article.user or request.user.is_staff():
        if article.status != status:
            if status == '1normal':
                article.status = status
                article.save()
            elif status == '7canceled' or status == '8full':
                article.status = status
                article.save()

                slots = article.slot_users.split(',')
                for slot in slots:
                    slotuser = User.objects.filter(username__iexact=slot).get()
                    if slotuser.profile.alarm_full:
                        if slotuser.profile.alarm_list != '':
                            slotuser.profile.alarm_list += ','
                        if status == '8full':
                            alarm_text = 'f:%d' % article.id
                        else:
                            alarm_text = 'c:%d' % article.id
                        slotuser.profile.alarm_list += alarm_text
                        slotuser.profile.alarm = True
                        slotuser.save()
        return redirect(article.get_article_url())
    else:
        return error_page(request)
