from boards.table import BoardTable

from django import template

register = template.Library()


@register.inclusion_tag('menu_main.html', takes_context=True)
def menu_main(context):
    """Main navigation menu"""
    user = context['request'].user
    logo = context['SITE_LOGO']
    info = context['SITE_INFO']
    my_bookmark = []

    if user.is_authenticated():
        if user.profile.bookmarks:
            bookmarks = user.profile.bookmarks.split(',')

            for bm in bookmarks:
                app, id = bm.split(':')
                if app == 'boards':
                    app_table = BoardTable()
                else:
                    continue
                my_bookmark.append(
                    [app_table.get_table_name(id), app_table.get_table_url(id)]
                )

    return {
        'user': user,
        'SITE_LOGO': logo,
        'SITE_INFO': info,
        'my_bookmark': my_bookmark,
    }


@register.inclusion_tag('menu_sub.html')
def menu_sub():
    """Sub navigation menu"""
    return {}


@register.inclusion_tag('menu_footer.html', takes_context=True)
def menu_footer(context):
    """Footer navigation menu"""
    admin_email = context['ADMIN_EMAIL']
    return {
        'ADMIN_EMAIL': admin_email,
    }
