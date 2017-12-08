"""portal URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.portal,
        name='portal',
    ),
    url(
        r'^(?P<page>\d+)$',
        views.portal,
        name='portal_redirection',
    ),
]
