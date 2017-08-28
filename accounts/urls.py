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
        r'^edit_user_info/$',
        views.edit_user_info,
        name='edit_user_info'
    ),
    url(
        r'^user_info/(?P<user>\w+)/$',
        views.user_info,
        name='user_info'
    ),
    url(
        r'^scrap/$',
        views.scrap_list,
        name='scrap_list_0'
    ),
    url(
        r'^scrap/(?P<page>\d+)/$',
        views.scrap_list,
        name='scrap_list'
    ),
    url(
        r'^delete_scrap/(?P<id>\d+)/$',
        views.delete_scrap,
        name='delete_scrap'
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
