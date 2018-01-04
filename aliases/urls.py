"""aliases URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.dashboard,
        name='dashboard'
    ),
    url(
        r'^(?P<alias>\w+)/$',
        views.click,
        name='click'
    ),
    url(
        r'^alias/new/$',
        views.new_alias,
        name='new_alias'
    ),
    url(
        r'^alias/edit/$',
        views.edit_alias,
        name='edit_alias'
    ),
    url(
        r'^alias/delete/$',
        views.delete_alias,
        name='delete_alias'
    ),
]
