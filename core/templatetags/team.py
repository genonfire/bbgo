from django import template
# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from teams.models import Team

register = template.Library()


@register.inclusion_tag('teams/show_team.html', takes_context=True)
def show_team(context, id):
    """Show team"""
    user = context['request'].user
    article = get_object_or_404(Team, pk=id)
    slot_users = article.slot_users.all()

    return {
        'user': user,
        'table': article.table,
        'article_id': article.id,
        'article_user': article.user,
        'slot_in': article.slot,
        'empty_slots': article.slot_total - article.slot,
        'slot_users': slot_users,
    }
