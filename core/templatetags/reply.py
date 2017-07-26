from boards.models import Board, Reply
from django import template

from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404

register = template.Library()


@register.inclusion_tag('boards/show_reply.html', takes_context=True)
def show_reply(context, id):
    """Show replies"""
    replies = Reply.objects.filter(article_id=id).annotate(
        custom_order=Case(
            When(reply_id=0, then='id'),
            default='reply_id',
            output_field=IntegerField(),
        )
    ).order_by('custom_order', 'id')
    user = context['request'].user
    article = get_object_or_404(Board, pk=id)

    return {
        'user': user,
        'article_user': article.user,
        'replies': replies,
        'count': replies.count()
    }
