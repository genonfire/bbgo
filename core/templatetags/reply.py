from boards.models import Reply
from django import template

register = template.Library()


@register.inclusion_tag('boards/show_reply.html')
def show_reply(id):
    """Show replies"""
    replies = Reply.objects.filter(article_id=id)

    return {
        'replies': replies,
        'count': replies.count()
    }
