"""portal URL Configuration"""

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        r'^robots\.txt$',
        TemplateView.as_view(
            template_name='robots.txt', content_type='text/plain')
    ),
    url(
        r'^sitemap\.xml$',
        TemplateView.as_view(template_name='sitemap.xml')
    ),
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
    url(
        r'^bbgo/$',
        views.bbgo,
        name='bbgo',
    ),
]
