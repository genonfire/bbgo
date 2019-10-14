"""recipes URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.show_recipes,
        name='show_recipes'
    ),
    url(
        r'^open/(?P<category>.*)/$',
        views.show_recipes,
        name='change_recipes'
    ),
    url(
        r'^instruction/$',
        views.instruction,
        name='instruction'
    ),
    url(
        r'^new/$',
        views.new_recipe,
        name='new_recipe'
    ),
    url(
        r'^(?P<id>\d+)/edit/$',
        views.edit_recipe,
        name='edit_recipe'
    ),
    url(
        r'^(?P<id>\d+)/delete/$',
        views.delete_recipe,
        name='delete_recipe'
    ),
    url(
        r'^edit_category/$',
        views.edit_category,
        name='edit_category'
    ),
    url(
        r'^save/$',
        views.save_order,
        name='save_order'
    ),
    url(
        r'^what_today/$',
        views.what_today,
        name='what_today'
    ),
    url(
        r'^new_category/$',
        views.new_category,
        name='new_category'
    ),
    url(
        r'^delete_category/$',
        views.delete_category,
        name='delete_category'
    ),
    url(
        r'^new_category/$',
        views.new_category,
        name='new_category'
    ),
    url(
        r'^save_category/$',
        views.save_category,
        name='save_category'
    ),
]
