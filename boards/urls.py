"""boards URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<table>\d+)/$',
        views.show_list,
        name='show_list_0'
    ),
    url(
        r'^(?P<table>\d+)/(?P<page>\d+)/$',
        views.show_list,
        name='show_list'
    ),
    url(
        r'^search/(?P<search_type>.*)/(?P<search_word>.*)/(?P<table>\d+)/(?P<page>\d+)/$',
        views.show_list,
        name='show_search_article',
    ),
    url(
        r'^search_reply/(?P<search_type>.*)/(?P<search_word>.*)/(?P<table>\d+)/(?P<page>\d+)/$',
        views.search_reply,
        name='search_reply',
    ),
    url(
        r'^delete_reply/(?P<id>\d+)/$',
        views.delete_reply,
        name='delete_reply'
    ),
    url(
        r'^(?P<table>\d+)/new/$',
        views.new_article,
        name='new_article'
    ),
    url(
        r'^article/(?P<id>\d+)/$',
        views.show_article,
        name='show_article'
    ),
    url(
        r'^article/(?P<id>\d+)/(?P<table>\d+)/$',
        views.show_article,
        name='show_table_article'
    ),
    url(
        r'^article/(?P<id>\d+)/edit/$',
        views.edit_article,
        name='edit_article'
    ),
    url(
        r'^article/(?P<id>\d+)/delete/$',
        views.delete_article,
        name='delete_article'
    ),
    url(
        r'^search/article/(?P<table>\d+)/(?P<search_type>\w+)/(?P<search_word>.*)/$',
        views.search_article,
        name='search_article'
    ),
]
