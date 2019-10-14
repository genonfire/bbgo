from django import template
from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404

from teams.models import Team, TeamReply

register = template.Library()


@register.inclusion_tag('teams/show_team_reply.html', takes_context=True)
def show_team_reply(context, id):
    """Show team replies"""
    replies = TeamReply.objects.filter(article_id=id).annotate(
        custom_order=Case(
            When(reply_id=0, then='id'),
            default='reply_id',
            output_field=IntegerField(),
        )
    ).order_by('custom_order', 'id')
    user = context['request'].user
    article = get_object_or_404(Team, pk=id)

    return {
        'user': user,
        'article_user': article.user,
        'replies': replies,
        'count': replies.count()
    }
