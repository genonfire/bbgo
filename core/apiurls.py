"""API URL Configuration"""

from django.conf.urls import url

from . import api

urlpatterns = [
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
        r'^alarm_off/$',
        api.alarm_off,
        name='alarm_off'
    ),
]
