"""recipes URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.summary,
        name='summary'
    ),
    url(
        r'^show/(?P<id>\d+)/$',
        views.show_paper,
        name='show_paper'
    ),
    url(
        r'^new/$',
        views.new_paper,
        name='new_paper'
    ),
    url(
        r'^inbox/(?P<page>\d+)/$',
        views.inbox,
        name='inbox',
        kwargs={'box': 'inbox'}
    ),
    url(
        r'^inbox_nc/(?P<page>\d+)/$',
        views.inbox,
        name='inbox_nc',
        kwargs={'box': 'inbox_nc'}
    ),
    url(
        r'^outbox/(?P<page>\d+)/$',
        views.inbox,
        name='outbox',
        kwargs={'box': 'outbox'}
    ),
    url(
        r'^archive/(?P<page>\d+)/$',
        views.inbox,
        name='archive',
        kwargs={'box': 'archive'}
    ),
    url(
        r'^search_inbox/(?P<search_type>.*)/(?P<search_word>.*)/(?P<page>\d+)/$',
        views.inbox,
        name='search_inbox',
        kwargs={'box': 'inbox'}
    ),
    url(
        r'^search_inbox_nc/(?P<search_type>.*)/(?P<search_word>.*)/(?P<page>\d+)/$',
        views.inbox,
        name='search_inbox_nc',
        kwargs={'box': 'inbox_nc'}
    ),
    url(
        r'^search_outbox/(?P<search_type>.*)/(?P<search_word>.*)/(?P<page>\d+)/$',
        views.inbox,
        name='search_outbox',
        kwargs={'box': 'outbox'}
    ),
    url(
        r'^search_archive/(?P<search_type>.*)/(?P<search_word>.*)/(?P<page>\d+)/$',
        views.inbox,
        name='search_archive',
        kwargs={'box': 'archive'}
    ),
]
