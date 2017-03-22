"""bbgo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', name='login', kwargs={'template_name': 'login.html'}),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': 'login'}),
    url(r'^accounts/passwordchange/', 'django.contrib.auth.views.password_change', {'post_change_redirect': 'login'}, name='passwordchange'),
    url(r'^$', 'board.views.show_list', name='board show list'),
    # Board
    url(r'^board/$', 'board.views.show_list', name='board show'),
    url(r'^board/(?P<table>\d+)/$', 'board.views.show_list', name='board show list'),
    url(r'^board/(?P<table>\d+)/(?P<page>\d+)/$', 'board.views.show_list', name='board show page'),
    url(r'^board/(?P<table>\d+)/new/$', 'board.views.new_article', name='board new'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
