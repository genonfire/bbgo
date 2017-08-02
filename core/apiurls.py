"""API URL Configuration"""

from django.conf.urls import url

from . import api

urlpatterns = [
    url(
        r'^check_duplication/$',
        api.check_duplication,
        name='check_duplication'
    ),
    url(
        r'^check_email/$',
        api.check_email,
        name='check_email',
    ),
    url(
        r'^check_validation/$',
        api.check_validation,
        name='check_validation'
    ),
    url(
        r'^like_article/$',
        api.like_article,
        name='like_article',
        kwargs={'liketype': 'like'}
    ),
    url(
        r'^dislike_article/$',
        api.like_article,
        name='dislike_article',
        kwargs={'liketype': 'dislike'}
    ),
    url(
        r'^like_users/$',
        api.like_users,
        name='like_users',
        kwargs={'liketype': 'like'}
    ),
    url(
        r'^dislike_users/$',
        api.like_users,
        name='dislike_users',
        kwargs={'liketype': 'dislike'}
    ),
    url(
        r'^like_reply/$',
        api.like_reply,
        name='like_reply',
        kwargs={'liketype': 'like'}
    ),
    url(
        r'^dislike_reply/$',
        api.like_reply,
        name='dislike_reply',
        kwargs={'liketype': 'dislike'}
    ),
    url(
        r'^write_reply/$',
        api.write_reply,
        name='write_reply',
    ),
    url(
        r'^reload_reply/$',
        api.reload_reply,
        name='reload_reply',
    ),
    url(
        r'^delete_reply/$',
        api.delete_reply,
        name='delete_reply',
    ),
    url(
        r'^toggle_bookmark/$',
        api.toggle_bookmark,
        name='toggle_bookmark',
    ),
    url(
        r'^alarm_off/$',
        api.alarm_off,
        name='alarm_off'
    ),
]
