from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='nickname')
def _nickname(user, is_authenticated=False):
    name = user
    if settings.ENABLE_NICKNAME and user.first_name:
        name = user.first_name

    if user.is_staff and not settings.DEBUG:
        return '<font color="#409BD1">%s</font>' % name
    elif is_authenticated:
        nametag = "<a href=javascript:void(0) onclick=\"javascript:id_menu(event, '%s');return false;\">%s</a>" % (user.username, name)
        return nametag
    else:
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
