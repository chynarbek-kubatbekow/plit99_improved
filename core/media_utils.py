import logging
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils._os import safe_join
from PIL import Image, ImageOps


MAX_IMAGE_SIZE = (1600, 1600)
logger = logging.getLogger(__name__)


def build_upload_path(directory, filename):
    extension = Path(filename).suffix.lower()
    if extension not in {'.jpg', '.jpeg', '.png', '.webp'}:
        extension = '.jpg'
    return f'{directory}/{uuid4().hex}{extension}'


def news_cover_upload_to(instance, filename):
    return build_upload_path('news/covers', filename)


def gallery_image_upload_to(instance, filename):
    return build_upload_path('gallery', filename)


def optimize_uploaded_image(uploaded_file):
    if not uploaded_file or getattr(uploaded_file, '_committed', False):
        return None

    try:
        uploaded_file.open('rb')
        with Image.open(uploaded_file) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

            has_alpha = image.mode in {'RGBA', 'LA'} or (
                image.mode == 'P' and 'transparency' in image.info
            )

            output = BytesIO()
            stem = Path(uploaded_file.name).stem or uuid4().hex

            if has_alpha:
                optimized = image.convert('RGBA')
                optimized.save(output, format='PNG', optimize=True, compress_level=7)
                extension = '.png'
            else:
                optimized = image.convert('RGB')
                optimized.save(
                    output,
                    format='JPEG',
                    quality=82,
                    optimize=True,
                    progressive=True,
                )
                extension = '.jpg'

        optimized_file = ContentFile(output.getvalue())
        optimized_file.name = f'{stem}{extension}'
        return optimized_file
    except Exception as exc:
        logger.warning(
            'Could not optimize uploaded image %s: %s',
            getattr(uploaded_file, 'name', 'unknown'),
            exc,
        )
        return None


def _safe_media_path(root, relative_path):
    if not relative_path:
        return None

    normalized = str(relative_path).replace('\\', '/').lstrip('/')
    try:
        return Path(safe_join(str(root), normalized))
    except ValueError:
        return None


def resolve_media_file_path(relative_path):
    if not relative_path:
        return None

    candidate = _safe_media_path(settings.MEDIA_ROOT, relative_path)
    if candidate and candidate.is_file():
        return candidate
    return None


def stored_media_exists(relative_path):
    return resolve_media_file_path(relative_path) is not None
