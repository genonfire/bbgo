# -*- coding: utf-8 -*-
from boards.table import BoardTable

from django import template
from django.core.urlresolvers import resolve

from teams.table import TeamTable

register = template.Library()


@register.inclusion_tag('menu_main.html', takes_context=True)
def menu_main(context):
    """Main navigation menu"""
    user = context['request'].user
    name = context['SITE_NAME']
    logo = context['SITE_LOGO']
    info = context['SITE_INFO']
    my_bookmark = []

    if user.is_authenticated():
        if user.profile.bookmarks:
            bookmarks = user.profile.bookmarks.split(',')

            for bm in bookmarks:
                app, id = bm.split('-')
                if app == 'boards':
                    app_table = BoardTable()
                elif app == 'teams':
                    app_table = TeamTable()
                else:
                    continue
                my_bookmark.append(
                    [app_table.get_table_name(id), app_table.get_table_url(id)]
                )

    return {
        'user': user,
        'SITE_NAME': name,
        'SITE_LOGO': logo,
        'SITE_INFO': info,
        'my_bookmark': my_bookmark,
    }


@register.inclusion_tag('menu_mobile.html', takes_context=True)
def menu_mobile(context):
    """Login menu for mobile"""
    request = context['request']
    id_max_length = context['ID_MAX_LENGTH']

    return {
        'user': request.user,
        'nexturl': request.path,
        'ID_MAX_LENGTH': id_max_length,
    }


@register.inclusion_tag('menu_sub.html', takes_context=True)
def menu_sub(context):
    """Sub navigation menu"""
    request = context['request']
    app = resolve(request.path).namespace
    name = context['SITE_NAME']
    info = context['SITE_INFO']
    blog_category = context['BLOG_CATEGORY']

    return {
        'app': app,
        'SITE_NAME': name,
        'SITE_INFO': info,
        'blog_category': blog_category,
    }


@register.inclusion_tag('menu_banner.html', takes_context=True)
def menu_banner(context):
    """Side banner"""
    request = context['request']
    app = resolve(request.path).namespace
    return {
        'app': app,
    }


@register.inclusion_tag('menu_setting.html')
def menu_setting():
    """Account setting menu"""
    return {}


@register.inclusion_tag('menu_footer.html', takes_context=True)
def menu_footer(context):
    """Footer navigation menu"""
    admin_email = context['ADMIN_EMAIL']
    site_name = context['SITE_NAME']
    return {
        'SITE_NAME': site_name,
        'ADMIN_EMAIL': admin_email,
    }
