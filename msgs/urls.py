"""msgs URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^inbox/(?P<page>\d+)/$',
        views.inbox,
        name='inbox'
    ),
    url(
        r'^conversation/(?P<user>\w+)/$',
        views.conversation,
        name='conversation'
    ),
    url(
        r'^append/(?P<user>\w+)/$',
        views.append,
        name='append'
    ),
    url(
        r'^send/(?P<user>\w+)/$',
        views.send,
        name='send'
    ),
    url(
        r'^delete_all/$',
        views.delete_all,
        name='delete_all'
    ),
    url(
        r'^delete_old/$',
        views.delete_old,
        name='delete_old'
    ),
    url(
        r'^delete_conversation/(?P<user>\w+)/$',
        views.delete_conversation,
        name='delete_conversation'
    ),
    url(
        r'^read_all/$',
        views.read_all,
        name='read_all'
    ),
]
