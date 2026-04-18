import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.utils._os import safe_join
from django.utils.http import http_date


MEDIA_CACHE_SECONDS = 60 * 60 * 24 * 30


def serve_media_file(request, path):
    if not settings.SERVE_MEDIA_FILES:
        raise Http404

    try:
        absolute_path = Path(safe_join(str(settings.MEDIA_ROOT), path))
    except ValueError as exc:
        raise Http404 from exc

    if not absolute_path.is_file():
        raise Http404

    stat = absolute_path.stat()
    content_type, encoding = mimetypes.guess_type(absolute_path.name)

    response = FileResponse(
        absolute_path.open('rb'),
        content_type=content_type or 'application/octet-stream',
    )
    response['Cache-Control'] = f'public, max-age={MEDIA_CACHE_SECONDS}, immutable'
    response['Content-Length'] = str(stat.st_size)
    response['Last-Modified'] = http_date(stat.st_mtime)
    response['X-Content-Type-Options'] = 'nosniff'
    if encoding:
        response['Content-Encoding'] = encoding
    return response
