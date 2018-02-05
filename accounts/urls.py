"""accounts URL Configuration"""

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(
        r'^login/$',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    url(
        r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
    url(
        r'^password_change/$',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    url(
        r'^password_reset/$',
        auth_views.PasswordResetView.as_view(),
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
        r'^edit_bookmarks/$',
        views.edit_bookmarks,
        name='edit_bookmarks'
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
    url(
        r'^dashboard_user/(?P<condition>.*)/(?P<page>\d+)/$',
        views.dashboard_user,
        name='dashboard_user'
    ),
]
