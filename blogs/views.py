# -*- coding: utf-8 -*-
from math import ceil

from core.utils import error_page, get_ipaddress, get_referer

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _

from models import Blog, Comment

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

    q = Q(status__iexact='1normal') & Q(category__iexact=post.category)

    next_post = Blog.objects.filter(q).order_by('-id').filter(id__gt=id)[:3]
    prev_post = Blog.objects.filter(q).order_by('-id').filter(id__lt=id)[:3]
    post_navi = []

    for p in next_post:
        post_navi.append(p)
    post_navi.append(post)
    for p in prev_post:
        post_navi.append(p)

    return render(
        request,
        "blogs/show_post.html",
        {
            'post': post,
            'status_text': status_text,
            'post_navi': post_navi,
        }
    )


@staff_member_required
def dashboard(request, condition='recent'):
    """Dashboard"""
    post_count = settings.DASHBOARD_POST_COUNT
    comment_count = settings.DASHBOARD_COMMENT_COUNT

    if condition == 'recent':
        order = '-id'
    elif condition == 'view':
        order = '-view_count'
    elif condition == 'like':
        order = '-like_count'
    elif condition == 'comment':
        order = '-comment_count'
    else:
        return error_page(request)

    posts = Blog.objects.filter(status='1normal').order_by(order)[:post_count]
    comments = Comment.objects.filter(
        status='1normal').order_by('-id')[:comment_count]

    total_posts = Blog.objects.filter(status='1normal').count()
    total_comments = Comment.objects.filter(status='1normal').count()
    total_spams = Comment.objects.filter(status='7spam').count()
    total_users = User.objects.count()

    return render(
        request,
        "blogs/dashboard.html",
        {
            'posts': posts,
            'comments': comments,
            'condition': condition,
            'total_posts': total_posts,
            'total_comments': total_comments,
            'total_spams': total_spams,
            'total_users': total_users,
        }
    )


@staff_member_required
def dashboard_post(request, status='all', category='all', page=1):
    """Dashboard"""
    list_count = settings.DASHBOARD_LIST_COUNT

    if int(page) < 1:
        return redirect('blogs:dashboard_post', status, category, 1)

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    qc = qs = Q()
    if category != 'all':
        qc = Q(category__iexact=category)
    if status != 'all':
        qs = Q(status__iexact=status)

    total = Blog.objects.filter(qc).filter(qs).count()
    lists = Blog.objects.filter(qc).filter(qs).order_by('-id')[start_at:end_at]

    count_all = Blog.objects.count()
    count_published = Blog.objects.filter(status__iexact='1normal').count()
    count_draft = Blog.objects.filter(status__iexact='2temp').count()
    count_pending = Blog.objects.filter(status__iexact='5hidden').count()
    count_deleted = Blog.objects.filter(status__iexact='6deleted').count()

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
        "blogs/dashboard_post.html",
        {
            'lists': lists,
            'total': total,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'mindex_begin': mindex_begin,
            'mindex_end': mindex_end + 1,
            'index_total': index_total,
            'status': status,
            'category': category,
            'count_all': count_all,
            'count_published': count_published,
            'count_draft': count_draft,
            'count_pending': count_pending,
            'count_deleted': count_deleted,
        }
    )


@staff_member_required
def dashboard_comment(request, status='all', page=1):
    """Dashboard comment"""
    list_count = settings.DASHBOARD_LIST_COUNT

    if int(page) < 1:
        return redirect('blogs:dashboard_comment', status, 1)

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count

    if status == 'all':
        q = Q()
    else:
        q = Q(status__iexact=status)

    total = Comment.objects.filter(q).count()
    lists = Comment.objects.filter(q).order_by('-id')[start_at:end_at]

    count_all = Comment.objects.count()
    count_normal = Comment.objects.filter(status__iexact='1normal').count()
    count_deleted = Comment.objects.filter(status__iexact='6deleted').count()
    count_spam = Comment.objects.filter(status__iexact='7spam').count()

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
        "blogs/dashboard_comment.html",
        {
            'lists': lists,
            'total': total,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'mindex_begin': mindex_begin,
            'mindex_end': mindex_end + 1,
            'index_total': index_total,
            'status': status,
            'count_all': count_all,
            'count_normal': count_normal,
            'count_deleted': count_deleted,
            'count_spam': count_spam,
        }
    )


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
def delete_post(request, id, stay):
    """Delete post"""
    post = get_object_or_404(Blog, pk=id)
    post.status = '6deleted'
    post.save()

    referer = get_referer(request)
    if stay:
        return redirect(referer)
    else:
        return redirect(post.get_absolute_url())


@staff_member_required
def restore_post(request, id):
    """Restore post"""
    post = get_object_or_404(Blog, pk=id)
    if post.status == '6deleted':
        post.status = '1normal'
        post.save()
    else:
        return error_page(request)

    referer = get_referer(request)
    return redirect(referer)


@staff_member_required
def delete_post_permanently(request, id):
    """Delete post permanently"""
    post = get_object_or_404(Blog, pk=id)
    if post.status == '6deleted':
        post.delete()
    else:
        return error_page(request)

    referer = get_referer(request)
    return redirect(referer)


@staff_member_required
def delete_comment(request, id):
    """Delete comment"""
    comment = get_object_or_404(Comment, pk=id)
    comment.status = '6deleted'
    comment.save()

    referer = get_referer(request)
    return redirect(referer)


@staff_member_required
def spam_comment(request, id):
    """Spam comment"""
    comment = get_object_or_404(Comment, pk=id)
    comment.status = '7spam'
    comment.save()

    referer = get_referer(request)
    return redirect(referer)


@staff_member_required
def restore_comment(request, id):
    """Restore comment"""
    comment = get_object_or_404(Comment, pk=id)
    if comment.status == '6deleted' or comment.status == '7spam':
        comment.status = '1normal'
        comment.save()
    else:
        return error_page(request)

    referer = get_referer(request)
    return redirect(referer)


@staff_member_required
def delete_comment_permanently(request, id):
    """Delete comment permanently"""
    comment = get_object_or_404(Comment, pk=id)
    if comment.status == '6deleted' or comment.status == '7spam':
        comment.delete()
    else:
        return error_page(request)

    referer = get_referer(request)
    return redirect(referer)


@staff_member_required
def empty_comment(request, status):
    """Empty comment"""
    if status == '6deleted' or status == '7spam':
        q = Q(status__iexact=status)
        Comment.objects.filter(q).all().delete()

    referer = get_referer(request)
    return redirect(referer)
