import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .media_utils import mirror_media_file


logger = logging.getLogger(__name__)
SNAPSHOT_FILENAME = 'site_content.json'


@dataclass(slots=True)
class SnapshotMediaFile:
    name: str = ''

    @property
    def storage(self):
        return default_storage

    @property
    def url(self):
        if not self.name:
            return ''
        return f'{settings.MEDIA_URL}{self.name}'

    def __bool__(self):
        return bool(self.name)


@dataclass(slots=True)
class SnapshotCategory:
    name: str
    slug: str
    color: str = 'badge-gray'
    order: int = 0


@dataclass(slots=True)
class SnapshotNews:
    title: str
    slug: str
    excerpt: str
    content: str
    cover_emoji: str
    cover_gradient: str
    is_featured: bool
    is_published: bool
    published_at: object
    created_at: object = None
    updated_at: object = None
    category: SnapshotCategory | None = None
    cover_image: SnapshotMediaFile | None = None

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


@dataclass(slots=True)
class SnapshotGalleryItem:
    title: str
    media_type: str
    video_url: str
    is_published: bool
    order: int
    created_at: object = None
    category: SnapshotCategory | None = None
    image: SnapshotMediaFile | None = None

    def __str__(self):
        return self.title or 'Медиа'


@dataclass(slots=True)
class SnapshotContent:
    news_categories: list[SnapshotCategory] = field(default_factory=list)
    gallery_categories: list[SnapshotCategory] = field(default_factory=list)
    news: list[SnapshotNews] = field(default_factory=list)
    gallery: list[SnapshotGalleryItem] = field(default_factory=list)


def _snapshot_path():
    return Path(settings.CONTENT_SNAPSHOT_DIR) / SNAPSHOT_FILENAME


def _project_snapshot_path():
    return Path(settings.PROJECT_CONTENT_SNAPSHOT_PATH)


def _empty_payload():
    return {
        'generated_at': timezone.now().isoformat(),
        'news_categories': [],
        'gallery_categories': [],
        'news': [],
        'gallery': [],
    }


def _serialize_datetime(value):
    return value.isoformat() if value else ''


def _parse_datetime(value):
    if not value:
        return None

    parsed = parse_datetime(value)
    if parsed is None:
        return None
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _datetime_sort_value(value):
    return value.timestamp() if value else float('-inf')


def _write_json_atomic(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(f'{path.suffix}.tmp')
    temp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    temp_path.replace(path)


def _serialize_from_database():
    from .models import GalleryCategory, GalleryItem, News, NewsCategory

    news_categories = list(NewsCategory.objects.all())
    gallery_categories = list(GalleryCategory.objects.all())
    news_items = list(News.objects.select_related('category').all())
    gallery_items = list(GalleryItem.objects.select_related('category').all())

    payload = _empty_payload()
    payload['news_categories'] = [
        {
            'name': category.name,
            'slug': category.slug,
            'color': category.color,
        }
        for category in news_categories
    ]
    payload['gallery_categories'] = [
        {
            'name': category.name,
            'slug': category.slug,
            'order': category.order,
        }
        for category in gallery_categories
    ]
    payload['news'] = []
    for item in news_items:
        cover_name = item.cover_image.name if item.cover_image else ''
        if cover_name:
            mirror_media_file(cover_name)

        payload['news'].append(
            {
                'title': item.title,
                'slug': item.slug,
                'excerpt': item.excerpt,
                'content': item.content,
                'cover_image': cover_name,
                'cover_emoji': item.cover_emoji,
                'cover_gradient': item.cover_gradient,
                'category_slug': item.category.slug if item.category else '',
                'is_featured': item.is_featured,
                'is_published': item.is_published,
                'published_at': _serialize_datetime(item.published_at),
                'created_at': _serialize_datetime(item.created_at),
                'updated_at': _serialize_datetime(item.updated_at),
            }
        )

    payload['gallery'] = []
    for item in gallery_items:
        image_name = item.image.name if item.image else ''
        if image_name:
            mirror_media_file(image_name)

        payload['gallery'].append(
            {
                'title': item.title,
                'media_type': item.media_type,
                'image': image_name,
                'video_url': item.video_url,
                'category_slug': item.category.slug if item.category else '',
                'is_published': item.is_published,
                'order': item.order,
                'created_at': _serialize_datetime(item.created_at),
            }
        )

    return payload


def export_content_snapshot():
    payload = _serialize_from_database()
    snapshot_path = _snapshot_path()
    _write_json_atomic(snapshot_path, payload)

    project_snapshot_path = _project_snapshot_path()
    try:
        _write_json_atomic(project_snapshot_path, payload)
    except OSError:
        logger.exception('Could not update project snapshot file %s.', project_snapshot_path)

    return snapshot_path


def safe_export_content_snapshot():
    try:
        return export_content_snapshot()
    except Exception:
        logger.exception('Could not refresh content snapshot.')
        return None


def _load_payload():
    candidate_paths = [_snapshot_path(), _project_snapshot_path()]
    for path in candidate_paths:
        if not path.is_file():
            continue

        try:
            raw = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            logger.exception('Could not read content snapshot from %s.', path)
            continue

        if isinstance(raw, dict):
            return raw

    return _empty_payload()


def load_content_snapshot():
    payload = _load_payload()

    news_categories = [
        SnapshotCategory(
            name=item.get('name', ''),
            slug=item.get('slug', ''),
            color=item.get('color', 'badge-gray'),
        )
        for item in payload.get('news_categories', [])
    ]
    gallery_categories = [
        SnapshotCategory(
            name=item.get('name', ''),
            slug=item.get('slug', ''),
            order=int(item.get('order', 0) or 0),
        )
        for item in payload.get('gallery_categories', [])
    ]

    news_categories_by_slug = {item.slug: item for item in news_categories}
    gallery_categories_by_slug = {item.slug: item for item in gallery_categories}

    news = [
        SnapshotNews(
            title=item.get('title', ''),
            slug=item.get('slug', ''),
            excerpt=item.get('excerpt', ''),
            content=item.get('content', ''),
            cover_emoji=item.get('cover_emoji', '📰'),
            cover_gradient=item.get('cover_gradient', 'linear-gradient(135deg,#0D3060,#1668C0)'),
            is_featured=bool(item.get('is_featured', False)),
            is_published=bool(item.get('is_published', True)),
            published_at=_parse_datetime(item.get('published_at')),
            created_at=_parse_datetime(item.get('created_at')),
            updated_at=_parse_datetime(item.get('updated_at')),
            category=news_categories_by_slug.get(item.get('category_slug', '')),
            cover_image=SnapshotMediaFile(item.get('cover_image', '')) if item.get('cover_image') else None,
        )
        for item in payload.get('news', [])
    ]
    news.sort(key=lambda item: _datetime_sort_value(item.published_at), reverse=True)

    gallery = [
        SnapshotGalleryItem(
            title=item.get('title', ''),
            media_type=item.get('media_type', 'photo'),
            image=SnapshotMediaFile(item.get('image', '')) if item.get('image') else None,
            video_url=item.get('video_url', ''),
            category=gallery_categories_by_slug.get(item.get('category_slug', '')),
            is_published=bool(item.get('is_published', True)),
            order=int(item.get('order', 0) or 0),
            created_at=_parse_datetime(item.get('created_at')),
        )
        for item in payload.get('gallery', [])
    ]
    gallery.sort(
        key=lambda item: (
            item.order,
            -_datetime_sort_value(item.created_at),
        )
    )

    return SnapshotContent(
        news_categories=news_categories,
        gallery_categories=gallery_categories,
        news=news,
        gallery=gallery,
    )
