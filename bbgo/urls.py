"""bbgo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('portal.urls')),
    url(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    url(r'^msgs/', include(('msgs.urls', 'msgs'), namespace='msgs')),
    url(r'^blogs/', include(('blogs.urls', 'blogs'), namespace='blogs')),
    url(r'^boards/', include(('boards.urls', 'boards'), namespace='boards')),
    url(r'^teams/', include(('teams.urls', 'teams'), namespace='teams')),
    url(r'^spams/', include(('spams.urls', 'spams'), namespace='spams')),
    url(r'^api/', include(('core.apiurls', 'api'), namespace='api')),
    url(r'^vaults/', include(('vaults.urls', 'vaults'), namespace='vaults')),
    url(r'^recipes/', include(
        ('recipes.urls', 'recipes'), namespace='recipes')),
    url(r'^a/', include(('aliases.urls', 'aliases'), namespace='aliases')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'django_summernote' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^summernote/', include('django_summernote.urls')))
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^trans/', include('rosetta.urls')))

if django.VERSION >= (2, 0):
    from django.urls import path
    urlpatterns.append(path('admin/', admin.site.urls))
else:
    urlpatterns.append(url('admin/', include(admin.site.urls)))
