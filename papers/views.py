# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from math import ceil

from core.utils import error_page

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PaperEditForm
from .models import Attachment, Paper, Person, Support


@login_required
def summary(request):
    """Summary"""
    ids = [paper.id for paper in Paper.objects.filter(completed=False).filter(
        cc__user=request.user) if paper.cc.last().user == request.user]
    mypapers = Paper.objects.filter(id__in=ids).order_by(
        '-updated_at')[:settings.SUMMARY_LIST_COUNT]

    proposals = Paper.objects.filter(user=request.user).order_by(
        '-updated_at')[:settings.SUMMARY_LIST_COUNT]

    if request.user.is_staff:
        q = Q()
    else:
        q = Q(completed=True)
    papers = Paper.objects.filter(q).order_by('-updated_at')[:settings.SUMMARY_LIST_COUNT]

    return render(
        request,
        "papers/summary.html",
        {
            'mypapers': mypapers,
            'proposals': proposals,
            'papers': papers,
        }
    )


@login_required
def show_paper(request, id):
    """Show paper"""
    paper = get_object_or_404(Paper, pk=id)
    if not request.user.is_staff and not paper.completed:
        cc = []
        for person in paper.cc.all():
            cc.append(person.user)

        if request.user not in cc:
            return error_page(request)

    return render(
        request,
        "papers/show_paper.html",
        {
            'paper': paper,
        }
    )


@login_required
def new_paper(request):
    """New paper"""
    if request.method == "POST":
        editform = PaperEditForm(request.POST)
        if editform.is_valid():
            paper = editform.save(commit=False)
            paper.user = request.user
            paper.save()

            files = request.FILES.getlist('files')
            for f in files:
                attachment = Attachment.objects.create(
                    file=f, content_type=f.content_type)
                paper.files.add(attachment)

            order = 1
            proposer = Person.objects.create(order=order, user=request.user)
            paper.cc.add(proposer)
            order += 1
            approver = Person.objects.create(order=order, user=paper.approver)
            paper.cc.add(approver)

            if editform.cleaned_data['support_names'] != '':
                names = editform.cleaned_data['support_names'].split(',')
                for name in names:
                    user = User.objects.filter(username__iexact=name).get()
                    order += 1
                    support = Support.objects.create(order=order, user=user)
                    paper.supporters.add(support)

            if editform.cleaned_data['notify_names'] != '':
                names = editform.cleaned_data['notify_names'].split(',')
                for name in names:
                    user = User.objects.filter(username__iexact=name).get()
                    order += 1
                    notifier = Person.objects.create(order=order, user=user)
                    paper.notifiers.add(notifier)

            return redirect('papers:summary')

    elif request.method == "GET":
        editform = PaperEditForm()

    return render(
        request,
        "papers/edit_paper.html",
        {
            'form': editform,
        }
    )


@login_required
def inbox(request, search_type='', search_word='', page=0, box=''):
    """Inbox"""
    if int(page) < 1:
        page = 1

    list_count = settings.INBOX_LIST_COUNT
    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    if box == 'inbox':
        sq = (~Q(user=request.user) & Q(cc__user=request.user))
    elif box == 'inbox_nc':
        sq = (~Q(user=request.user) & Q(cc__user=request.user) & Q(
            completed=False))
    elif box == 'outbox':
        sq = Q(user=request.user)
    elif box == 'archive':
        if request.user.is_staff:
            sq = Q()
        else:
            sq = Q(completed=True)
    else:
        return error_page(request)

    if search_type == 'title':
        q = sq & Q(title__icontains=search_word)
    elif search_type == 'subjectcontent':
        q = sq & (
            Q(title__icontains=search_word) |
            Q(content__icontains=search_word)
        )
    elif search_type == 'proposer':
        q = sq & (
            Q(user__username__icontains=search_word) |
            Q(user__last_name__icontains=search_word)
        )
    elif search_type == 'approver':
        q = sq & (
            Q(approver__username__icontains=search_word) |
            Q(approver__last_name__icontains=search_word)
        )
    else:
        q = sq

    total = Paper.objects.filter(q).distinct().count()
    lists = Paper.objects.filter(q).distinct().order_by(
        '-updated_at')[start_at:end_at]

    index_total = int(ceil(float(total) / list_count))
    index_begin = int(current_page / 10) * 10 + 1
    index_end = mindex_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9
    mindex_begin = int(current_page / 5) * 5 + 1
    if mindex_end - mindex_begin >= 5:
        mindex_end = mindex_begin + 4

    return render(
        request,
        "papers/show_inbox.html",
        {
            'lists': lists,
            'total': total,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'mindex_begin': mindex_begin,
            'mindex_end': mindex_end + 1,
            'index_total': index_total,
            'search_type': search_type,
            'search_word': search_word,
            'box': box,
        }
    )
