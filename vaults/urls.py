"""vaults URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.open_vault,
        name='open_vault'
    ),
    url(
        r'^open/(?P<category>.*)/$',
        views.open_vault,
        name='change_vault'
    ),
    url(
        r'^new/$',
        views.new_vault,
        name='new_vault'
    ),
    url(
        r'^(?P<id>\d+)/edit/$',
        views.edit_vault,
        name='edit_vault'
    ),
    url(
        r'^(?P<id>\d+)/delete/$',
        views.delete_vault,
        name='delete_vault'
    ),
    url(
        r'^save/$',
        views.save_order,
        name='save_order'
    ),
    url(
        r'^new_key/$',
        views.new_key,
        name='new_key'
    ),
    url(
        r'^edit_key/$',
        views.edit_key,
        name='edit_key'
    ),
    url(
        r'^check_key/$',
        views.check_key,
        name='check_key'
    ),
    url(
        r'^extend_expiry/$',
        views.extend_expiry,
        name='extend_expiry'
    )
]
