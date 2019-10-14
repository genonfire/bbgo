from django import template
from django.conf import settings
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name='nickname')
def _nickname(user, is_authenticated=False):
    name = user
    if settings.ENABLE_NICKNAME and user.first_name:
        name = user.first_name

    if is_authenticated:
        nametag = "<a href=javascript:void(0) onclick=\"javascript:id_menu(event, '%s');return false;\">%s</a>" % (user.username, name)
        return nametag
    else:
        return name


@register.filter(name='realname')
def _realname(user, is_authenticated=False):
    name = user
    if user.last_name:
        name = user.last_name

    if is_authenticated:
        nametag = "<a href=javascript:void(0) onclick=\"javascript:id_menu(event, '%s');return false;\">%s</a>" % (user.username, name)
        return nametag
    else:
        return name


@register.filter(name='textnickname')
def _textnickname(username, is_authenticated=False):
    name = username
    if settings.ENABLE_NICKNAME:
        user = User.objects.filter(username__iexact=username)
        if user:
            if user[0].first_name:
                name = user[0].first_name
    return name


@register.filter(name='id')
def _id(user, table):
    platform = int(table)
    if platform == 1:
        return user.profile.id1
    elif platform == 2:
        return user.profile.id2
    elif platform == 3:
        return user.profile.id3


@register.filter(name='portrait')
def _portrait(username):
    username_tag = username
    user = User.objects.filter(username__iexact=username)
    if user and user[0].profile.portrait:
        username_tag = "<img src='%s' width=20px height=20px> %s" % (user[0].profile.portrait.url, username)

    return username_tag
