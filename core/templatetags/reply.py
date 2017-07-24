from boards.models import Reply
from django import template

from django.db.models import Case, IntegerField, When

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

    return {
        'user': user,
        'replies': replies,
        'count': replies.count()
    }
