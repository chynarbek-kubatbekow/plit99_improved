from io import BytesIO
from pathlib import Path
from uuid import uuid4

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


MAX_IMAGE_SIZE = (1600, 1600)


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
