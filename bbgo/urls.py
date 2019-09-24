from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [path('trans/', include('rosetta.urls'))]

if settings.LOCAL_SERVER:
    if 'rest_framework' in settings.INSTALLED_APPS:
        urlpatterns += [
            path('restapi/', include(
                'rest_framework.urls', namespace='rest_framework'))
        ]

    if 'drf_yasg' in settings.INSTALLED_APPS:
        from rest_framework import permissions
        from drf_yasg.views import get_schema_view
        from drf_yasg import openapi

        schema_view = get_schema_view(
            openapi.Info(
                title="bbgo APIs",
                default_version='beta',
            ),
            public=True,
            permission_classes=(permissions.AllowAny,),
        )

        urlpatterns += [
            url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
                cache_timeout=0), name='schema-json'),
            url(r'^swagger/$', schema_view.with_ui(
                'swagger', cache_timeout=0), name='schema-swagger-ui'),
            url(r'^redoc/$', schema_view.with_ui(
                'redoc', cache_timeout=0), name='schema-redoc'),
        ]
