"""boards URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.show_list,
        name='show'
    ),
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
        r'^article/(?P<id>\d+)/$',
        views.show_article,
        name='show_article'
    ),
    url(
        r'^(?P<table>\d+)/new/$',
        views.new_article,
        name='new_article'
    ),
]
