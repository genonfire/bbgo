# -*- coding: utf-8 -*-
from math import ceil

from core.utils import error_page, get_ipaddress

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _

from models import Blog

from .forms import BlogEditForm


def show_blogs(request, search_type='', search_word='', page=0):
    """Show blogs"""
    list_count = settings.BLOG_LIST_COUNT

    if int(page) < 1:
        return redirect('blogs:show_blogs', page=1)

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    sq = Q(status='1normal')
    mq = (sq | Q(status='2temp'))
    if search_type == 'category':
        q = sq & Q(category__iexact=search_word)
    elif search_type == 'tag':
        q = sq & Q(tags__icontains=search_word)
    elif search_type == 'all':
        q = sq & (Q(tags__icontains=search_word) | Q(
            content__icontains=search_word) | Q(title__icontains=search_word))
    else:
        q = sq

    total = Blog.objects.filter(q).count()
    lists = Blog.objects.filter(q).order_by('-id')[start_at:end_at]

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
        "blogs/show_blogs.html",
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
        }
    )


def show_post(request, id):
    """Show post"""
    post = get_object_or_404(Blog, pk=id)

    if post.status == '5hidden' and not request.user.is_staff:
        errormsg = _('status_pending')
        return error_page(request, errormsg)
    elif post.status == '6deleted' and not request.user.is_staff:
        errormsg = _('status_deleted')
        return error_page(request, errormsg)
    elif post.status == '2temp' and not request.user == post.user:
        return error_page(request)

    post.view_count += 1
    post.save()

    if post.status != '1normal':
        status_text = post.get_status_text()
    else:
        status_text = ''

    return render(
        request,
        "blogs/show_post.html",
        {
            'post': post,
            'status_text': status_text,
        }
    )


@staff_member_required
def dashboard(reqeust, page=0):
    """Dashboard"""


@staff_member_required
def new_post(request):
    """New post"""
    if request.method == "POST":
        editform = BlogEditForm(request.POST, request.FILES)
        if editform.is_valid():
            post = editform.save(commit=False)
            post.user = request.user
            post.ip = get_ipaddress(request)
            post.save()

            return redirect(post.get_post_url())
    elif request.method == "GET":
        editform = BlogEditForm()

    category_choices = settings.BLOG_CATEGORY

    return render(
        request,
        "blogs/edit_post.html",
        {
            'form': editform,
            'edit_type': 'new',
            'category_choices': category_choices,
        }
    )


@staff_member_required
def edit_post(request, id):
    """Edit post"""
    post = get_object_or_404(Blog, pk=id)
    edit_type = 'edit'

    if request.method == "POST":
        editform = BlogEditForm(request.POST, request.FILES, instance=post)
        if editform.is_valid():
            post = editform.save(commit=False)

            if post.status == '2temp':
                post.created_at = timezone.now()
                post.save()
                return redirect(post.get_edit_url())

            post.modified_at = timezone.now()
            post.save()

            return redirect(post.get_post_url())
    elif request.method == "GET":
        editform = BlogEditForm(instance=post)

        if post.status == '2temp':
            edit_type = 'temp'

    category_choices = settings.BLOG_CATEGORY

    return render(
        request,
        'blogs/edit_post.html',
        {
            'form': editform,
            'edit_type': edit_type,
            'category_choices': category_choices,
            'category': post.category,
            'created_at': post.created_at,
            'featured_image': post.image,
        }
    )


@staff_member_required
def delete_post(request, id):
    """Delete post"""
    post = get_object_or_404(Blog, pk=id)

    if request.user == post.user or request.user.is_staff:
        post.status = '6deleted'
        post.save()
    else:
        return error_page(request)

    return redirect(post.get_absolute_url())
