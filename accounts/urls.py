"""accounts URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'accounts/login.html'}
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
    ),
    url(
        r'^password_change/$',
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
    url(
        r'^setting/$',
        views.setting,
        name='setting'
    ),
    url(
        r'^user_info/$',
        views.user_info,
        name='user_info'
    ),
    url(
        r'^show_deactivate_account/$',
        views.show_deactivate_account,
        name='show_deactivate_account',
    ),
    url(
        r'^deactivate_account/$',
        views.deactivate_account,
        name='deactivate_account',
    ),
]
