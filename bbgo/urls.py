from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [path('trans/', include('rosetta.urls'))]

if 'rest_framework_swagger' in settings.INSTALLED_APPS:
    urlpatterns += [path('api/docs/', get_swagger_view(title='APIs'))]
