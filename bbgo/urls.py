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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import javascript_catalog

from jsi18ncache.views import javascript_catalog_cache

js_info_dict = {
    'packages': ('',),
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^jsi18n-debug/$',
        javascript_catalog,
        js_info_dict,
    ),
    url(
        r'^.*/jsi18n/$',
        javascript_catalog_cache,
        js_info_dict,
    ),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('portal.urls')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^msgs/', include('msgs.urls', namespace='msgs')),
    url(r'^blogs/', include('blogs.urls', namespace='blogs')),
    url(r'^boards/', include('boards.urls', namespace='boards')),
    url(r'^teams/', include('teams.urls', namespace='teams')),
    url(r'^spams/', include('spams.urls', namespace='spams')),
    url(r'^api/', include('core.apiurls', namespace='api')),
    url(r'^vaults/', include('vaults.urls', namespace='vaults')),
    url(r'^recipes/', include('recipes.urls', namespace='recipes')),
    url(r'^a/', include('aliases.urls', namespace='aliases')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'django_summernote' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^summernote/', include('django_summernote.urls')))
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^trans/', include('rosetta.urls')))
