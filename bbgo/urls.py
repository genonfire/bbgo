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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import javascript_catalog

js_info_dict = {
    'packages': ('',),
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(
        r'^accounts/login/',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'login.html'}
    ),
    url(
        r'^accounts/logout/',
        'django.contrib.auth.views.logout',
        name='logout',
        # kwargs={'next_page': 'login'}
    ),
    url(
        r'^accounts/passwordchange/',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect': 'login'},
        name='passwordchange'
    ),
    url(
        r'^accounts/passwordreset/$',
        'django.contrib.auth.views.password_reset',
        name='passwordreset'
    ),
    # url(
    #     r'^accounts/signup/',
    #     ,
    #     name='signup'
    # ),
    url(
        r'^jsi18n/$',
        javascript_catalog,
        js_info_dict,
        name='javascript-catalog'
    ),
    url(r'^boards/', include('boards.urls', namespace='boards')),
    url(r'^api/', include('core.apiurls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'django_summernote' in settings.INSTALLED_APPS:
    urlpatterns.append(url(
        r'^summernote/', include('django_summernote.urls')
    ))
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns.append(url(
        r'^trans/', include('rosetta.urls'),
    ))
