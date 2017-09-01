"""teams URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<table>\d+)/$',
        views.recruitment,
        name='recruitment_0'
    ),
    url(
        r'^(?P<table>\d+)/(?P<page>\d+)/$',
        views.recruitment,
        name='recruitment'
    ),
    url(
        r'^recruitment/(?P<id>\d+)/$',
        views.show_recruitment,
        name='show_recruitment'
    ),
    url(
        r'^(?P<table>\d+)/new/$',
        views.new_recruitment,
        name='new_recruitment'
    ),
    url(
        r'^recruitment/(?P<id>\d+)/edit/$',
        views.edit_recruitment,
        name='edit_recruitment'
    ),
    url(
        r'^recruitment/(?P<id>\d+)/status/(?P<status>\w+)/$',
        views.change_status,
        name='change_status'
    ),
]
