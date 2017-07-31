from django import template

register = template.Library()


@register.filter(name='is_stared')
def _is_stared(user, app_id):
    profile = user.profile
    bookmarks = profile.bookmarks.split(',')

    if app_id not in bookmarks:
        return False
    else:
        return True
