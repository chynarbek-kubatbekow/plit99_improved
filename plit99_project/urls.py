from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

from core.media_views import serve_media_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.SERVE_MEDIA_FILES:
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve_media_file,
        ),
    ]
