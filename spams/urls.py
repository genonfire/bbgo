"""spams URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.setting,
        name='setting'
    ),
    url(
        r'^add_ip/$',
        views.add_ip,
        name='add_ip'
    ),
    url(
        r'^add_word/$',
        views.add_word,
        name='add_word'
    ),
    url(
        r'^delete_ip/$',
        views.delete_ip,
        name='delete_ip'
    ),
    url(
        r'^delete_word/$',
        views.delete_word,
        name='delete_word'
    ),
    url(
        r'^register_ip/$',
        views.register_ip,
        name='register_ip'
    ),
]
