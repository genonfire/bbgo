"""accounts URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^login/',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'registration/login.html'}
    ),
    url(
        r'^logout/',
        'django.contrib.auth.views.logout',
        name='logout',
    ),
    url(
        r'^password_change/',
        'django.contrib.auth.views.password_change',
        name='password_change'
    ),
    url(
        r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset'
    ),
    url(
        r'^signup/$',
        views.sign_up,
        name='signup'
    ),
]
