# -*- coding: utf-8 -*-
from boards.models import Board

from django import template
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

register = template.Library()


@register.filter(name='article_info')
def _article_info(id):
    article = get_object_or_404(Board, pk=id)
    subject = article.subject
    count = article.reply_count
    article_url = reverse_lazy('boards:show_article', args=[article.id])

    return "<a href='%s'>%s</a><span class='bloginfo'>%d</span>" % (article_url, subject, count)
