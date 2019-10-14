# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from math import ceil

from core.utils import error_page, get_ipaddress

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _

from .forms import MsgForm
from .models import Msg


@login_required
def inbox(request, page=1):
    """Msg inbox"""
    list_count = settings.MSG_LIST_COUNT

    current_page = int(page) - 1
    start_at = current_page * list_count
    end_at = start_at + list_count
    old_at = timezone.now() - timezone.timedelta(
        days=settings.OLD_MSG_THRESHOLD)

    q_sender = Q(sender__username__iexact=request.user.username) & Q(
        sender_status='1normal')
    msgs = Msg.objects.filter(q_sender).order_by('-id')
    senders = msgs.values('recipient').distinct().values_list(
        'recipient', flat=True)

    old_msgs = msgs.filter(created_at__lte=old_at)
    old_total = old_msgs.count()

    q_recipient = Q(recipient__username__iexact=request.user.username) \
        & (Q(recipient_status='1normal') | Q(recipient_status='2read'))
    msgs = Msg.objects.filter(q_recipient).order_by('-id')
    recipients = msgs.values('sender').distinct().values_list(
        'sender', flat=True)

    old_msgs = msgs.filter(created_at__lte=old_at)
    old_total += old_msgs.count()

    q = q_sender | q_recipient

    x = list(senders) + list(recipients)
    setx = set(x)
    user_ids = sorted(setx, key=x.index)[start_at:end_at]
    total = len(setx)

    my_msgs = []
    for user_id in user_ids:
        user = get_object_or_404(User, pk=user_id)
        q_user = Q(sender__username__iexact=user.username) | Q(
            recipient__username__iexact=user.username)
        last_msg = Msg.objects.filter(q).filter(q_user).order_by('-id')[:1]
        my_msgs.append([user, last_msg[0]])

    index_total = int(ceil(float(total) / list_count))
    index_begin = int(current_page / 10) * 10 + 1
    index_end = mindex_end = index_total
    if index_end - index_begin >= 10:
        index_end = index_begin + 9
    mindex_begin = int(current_page / 5) * 5 + 1
    if mindex_end - mindex_begin >= 5:
        mindex_end = mindex_begin + 4

    unread_msgs = Msg.objects.filter(recipient__username__iexact=request.user.username).filter(recipient_status='1normal')
    unread_total = unread_msgs.count()
    if request.user.profile.msg_count is not unread_total:
        request.user.profile.msg_count = unread_total
        request.user.profile.save()

    return render(
        request,
        "msgs/inbox.html",
        {
            'msgs': my_msgs,
            'total': total,
            'unread_total': unread_total,
            'old_total': old_total,
            'page': current_page + 1,
            'index_begin': index_begin,
            'index_end': index_end + 1,
            'mindex_begin': mindex_begin,
            'mindex_end': mindex_end + 1,
            'index_total': index_total,
        }
    )


@login_required
def conversation(request, user):
    """Conversation"""
    try:
        other = User.objects.filter(username__iexact=user).get()
    except ObjectDoesNotExist:
        errormsg = _('User does not exist.')
        return error_page(request, errormsg)

    if request.user == other:
        errormsg = _('Cannot send message to yourself.')
        return error_page(request, errormsg)

    if request.method == "POST":
        msgform = MsgForm(request.POST)
        if msgform.is_valid():
            msg = msgform.save(commit=False)
            msg.sender = request.user
            msg.recipient = other
            msg.ip = get_ipaddress(request)
            msg.save()
            other.profile.msg_count += 1
            other.profile.save()

            return redirect('msgs:conversation', user=other)
        else:
            errormsg = _('Form validation Failure')
            return error_page(request, errormsg)
    else:
        q = (Q(sender__username__iexact=other.username) & Q(
            recipient__username__iexact=request.user.username) & (Q(
                recipient_status='1normal') | Q(recipient_status='2read'))) | \
            (Q(sender__username__iexact=request.user.username) & Q(
                recipient__username__iexact=other.username) & Q(
                    sender_status='1normal'))

        msgs = Msg.objects.filter(q).order_by('id')

        unread_msgs = msgs.filter(recipient_status='1normal').filter(
            recipient__username__iexact=request.user.username)
        for um in unread_msgs:
            um.recipient_status = '2read'
            um.save()

        return render(
            request,
            "msgs/conversation.html",
            {
                'msgs': msgs,
                'other': other,
            }
        )


@login_required
def send(request, user):
    """Send message"""
    try:
        recipient = User.objects.filter(username__iexact=user).get()
    except ObjectDoesNotExist:
        errormsg = _('User does not exist.')
        return error_page(request, errormsg)

    if request.user == recipient:
        errormsg = _('Cannot send message to yourself.')
        return error_page(request, errormsg)

    if request.method == "POST":
        msgform = MsgForm(request.POST)
        if msgform.is_valid():
            message = msgform.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.ip = get_ipaddress(request)
            message.save()
            recipient.profile.msg_count += 1
            recipient.profile.save()

            return redirect('msgs:inbox', page=1)
        else:
            msg = _('Form validation Failure')

    elif request.method == "GET":
        msg = ""
        msgform = MsgForm(instance=request.user.profile)

    return render(
        request,
        "msgs/send_msg.html",
        {
            'msgform': msgform,
            'recipient': recipient,
            'msg': msg,
        }
    )


@login_required
def delete_all(request):
    """Delete all messages"""
    q_sender = Q(sender__username__iexact=request.user.username) & Q(
        sender_status='1normal')
    msgs = Msg.objects.filter(q_sender)
    for msg in msgs:
        msg.sender_status = '6deleted'
        msg.save()

    q_recipient = Q(recipient__username__iexact=request.user.username) \
        & (Q(recipient_status='1normal') | Q(
            recipient_status='2read'))
    msgs = Msg.objects.filter(q_recipient)
    for msg in msgs:
        msg.recipient_status = '6deleted'
        msg.save()

    return redirect('msgs:inbox', page=1)


@login_required
def delete_old(request):
    """Delete old messages"""
    old_at = timezone.now() - timezone.timedelta(
        days=settings.OLD_MSG_THRESHOLD)

    q_sender = Q(sender__username__iexact=request.user.username) & Q(
        sender_status='1normal') & Q(created_at__lte=old_at)
    msgs = Msg.objects.filter(q_sender)
    for msg in msgs:
        msg.sender_status = '6deleted'
        msg.save()

    q_recipient = Q(recipient__username__iexact=request.user.username) \
        & (Q(recipient_status='1normal') | Q(
            recipient_status='2read')) & Q(created_at__lte=old_at)
    msgs = Msg.objects.filter(q_recipient)
    for msg in msgs:
        msg.recipient_status = '6deleted'
        msg.save()

    return redirect('msgs:inbox', page=1)


@login_required
def delete_conversation(request, user):
    """Delete conversation"""
    q_sender = Q(sender__username__iexact=request.user.username) & Q(
        recipient__username__iexact=user) & Q(
            sender_status='1normal')
    msgs = Msg.objects.filter(q_sender)
    for msg in msgs:
        msg.sender_status = '6deleted'
        msg.save()

    q_recipient = Q(sender__username__iexact=user) & Q(
        recipient__username__iexact=request.user.username) & (Q(
            recipient_status='1normal') | Q(recipient_status='2read'))
    msgs = Msg.objects.filter(q_recipient)
    for msg in msgs:
        msg.recipient_status = '6deleted'
        msg.save()

    return redirect('msgs:inbox', page=1)


@login_required
def read_all(request):
    """Read all messages"""
    msgs = Msg.objects.filter(recipient__username__iexact=request.user.username).filter(recipient_status='1normal')

    for msg in msgs:
        msg.recipient_status = '2read'
        msg.save()

    return redirect('msgs:inbox', page=1)
