from django import template
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from teams.models import Team

register = template.Library()


@register.inclusion_tag('teams/show_team.html', takes_context=True)
def show_team(context, id):
    """Show team"""
    user = context['request'].user
    article = get_object_or_404(Team, pk=id)
    table = article.table
    slot_in = article.slot
    slot_total = article.slot_total
    slot_users = []

    if slot_in > 1:
        slots = article.slot_users.split(',')
        for slot in slots:
            slot_user = User.objects.filter(username__iexact=slot).get()
            slot_users.append([slot_user])

    return {
        'user': user,
        'table': table,
        'article_id': article.id,
        'article_user': article.user,
        'slot_in': slot_in,
        'slot_total': slot_total,
        'slot_users': slot_users,
    }
