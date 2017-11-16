"""blogs URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.show_blogs,
        name='blog_home'
    ),
    url(
        r'^(?P<page>\d+)/$',
        views.show_blogs,
        name='show_blogs'
    ),
    url(
        r'^search/(?P<search_type>.*)/(?P<search_word>.*)/(?P<page>\d+)/$',
        views.show_blogs,
        name='search_post',
    ),
    url(
        r'^dashboard/(?P<page>\d+)/$',
        views.dashboard,
        name='dashboard'
    ),
    url(
        r'^new/$',
        views.new_post,
        name='new_post'
    ),
    url(
        r'^post/(?P<id>\d+)/$',
        views.show_post,
        name='show_post'
    ),
    url(
        r'^post/(?P<id>\d+)/edit/$',
        views.edit_post,
        name='edit_post'
    ),
    url(
        r'^post/(?P<id>\d+)/delete/$',
        views.delete_post,
        name='delete_post'
    ),
]
