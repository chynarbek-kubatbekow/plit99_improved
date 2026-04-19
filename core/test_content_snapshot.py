import json
import shutil
import uuid
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import OperationalError
from django.test import TestCase
from PIL import Image

from .content_snapshot import export_content_snapshot
from .models import GalleryCategory, GalleryItem, News, NewsCategory


def build_test_image(width=1800, height=1200, color=(40, 90, 160)):
    image = Image.new('RGB', (width, height), color=color)
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=92)
    return buffer.getvalue()


def make_temp_dir(base_name):
    path = Path.cwd() / f'.{base_name}' / uuid.uuid4().hex
    path.mkdir(parents=True, exist_ok=True)
    return path


class ContentSnapshotTests(TestCase):
    def test_admin_news_add_page_loads_with_cookie_sessions(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-pass-123',
        )

        with self.settings(
            SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
            MESSAGE_STORAGE='django.contrib.messages.storage.cookie.CookieStorage',
            SECURE_SSL_REDIRECT=False,
        ):
            self.client.force_login(user)
            response = self.client.get('/admin/core/news/add/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"', html=False)

    def test_admin_returns_maintenance_page_when_database_breaks(self):
        user = get_user_model().objects.create_superuser(
            username='guard-admin',
            email='guard-admin@example.com',
            password='test-pass-123',
        )

        with self.settings(
            SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
            MESSAGE_STORAGE='django.contrib.messages.storage.cookie.CookieStorage',
            SECURE_SSL_REDIRECT=False,
        ):
            self.client.force_login(user)
            with patch.object(User, 'has_module_perms', side_effect=OperationalError('db is down')):
                response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, 'Админка временно недоступна', status_code=503)

    def test_snapshot_export_returns_empty_payload_when_tables_are_unavailable(self):
        with patch('core.models.NewsCategory.objects.all', side_effect=OperationalError('no such table')):
            snapshot_path = export_content_snapshot()

        payload = json.loads(snapshot_path.read_text(encoding='utf-8'))
        self.assertEqual(payload['news_categories'], [])
        self.assertEqual(payload['gallery_categories'], [])
        self.assertEqual(payload['news'], [])
        self.assertEqual(payload['gallery'], [])

    def test_snapshot_and_media_mirror_support_public_fallback(self):
        snapshot_dir = make_temp_dir('test-snapshots')
        media_root = make_temp_dir('test-media-primary')
        mirror_root = make_temp_dir('test-media-mirror')

        try:
            with self.settings(
                CONTENT_SNAPSHOT_DIR=snapshot_dir,
                PROJECT_CONTENT_SNAPSHOT_PATH=snapshot_dir / 'project-site_content.json',
                MEDIA_ROOT=media_root,
                LOCAL_MEDIA_MIRROR_ROOT=mirror_root,
                LOCAL_MEDIA_MIRROR_ENABLED=True,
                SERVE_MEDIA_FILES=True,
                SECURE_SSL_REDIRECT=False,
            ):
                upload = SimpleUploadedFile(
                    'snapshot-news.jpg',
                    build_test_image(),
                    content_type='image/jpeg',
                )
                gallery_upload = SimpleUploadedFile(
                    'snapshot-gallery.jpg',
                    build_test_image(color=(90, 60, 150)),
                    content_type='image/jpeg',
                )

                with self.captureOnCommitCallbacks(execute=True):
                    news_category = NewsCategory.objects.create(
                        name='События',
                        slug='events',
                        color='badge-ocean',
                    )
                    gallery_category = GalleryCategory.objects.create(
                        name='Учёба',
                        slug='study',
                        order=1,
                    )
                    news = News.objects.create(
                        title='Snapshot News',
                        slug='snapshot-news',
                        excerpt='Snapshot excerpt',
                        content='Snapshot full content',
                        category=news_category,
                        cover_image=upload,
                        is_featured=True,
                    )
                    gallery_item = GalleryItem.objects.create(
                        title='Snapshot Gallery',
                        media_type='photo',
                        image=gallery_upload,
                        category=gallery_category,
                        is_published=True,
                        order=2,
                    )

                snapshot_path = snapshot_dir / 'site_content.json'
                self.assertTrue(snapshot_path.is_file())

                snapshot_payload = json.loads(snapshot_path.read_text(encoding='utf-8'))
                self.assertEqual(snapshot_payload['news'][0]['slug'], 'snapshot-news')
                self.assertEqual(snapshot_payload['gallery'][0]['title'], 'Snapshot Gallery')

                mirror_news_path = mirror_root / news.cover_image.name
                mirror_gallery_path = mirror_root / gallery_item.image.name
                self.assertTrue(mirror_news_path.is_file())
                self.assertTrue(mirror_gallery_path.is_file())

                source_news_path = media_root / news.cover_image.name
                source_news_path.unlink()
                media_response = self.client.get(f'/media/{news.cover_image.name}')
                self.assertEqual(media_response.status_code, 200)

                with patch('core.views.NewsCategory.objects.all', side_effect=OperationalError('db is down')):
                    news_response = self.client.get('/news/')
                self.assertEqual(news_response.status_code, 200)
                self.assertContains(news_response, 'Snapshot News')

                with patch('core.views.GalleryCategory.objects.all', side_effect=OperationalError('db is down')):
                    gallery_response = self.client.get('/gallery/')
                self.assertEqual(gallery_response.status_code, 200)
                self.assertContains(gallery_response, 'Snapshot Gallery')

                with patch('core.views.NewsCategory.objects.all', side_effect=OperationalError('db is down')):
                    media_hub_response = self.client.get('/media/')
                self.assertEqual(media_hub_response.status_code, 200)
                self.assertContains(media_hub_response, 'Snapshot News')
                self.assertContains(media_hub_response, 'Snapshot Gallery')

                with patch('core.views.get_object_or_404', side_effect=OperationalError('db is down')):
                    detail_response = self.client.get('/news/snapshot-news/')
                self.assertEqual(detail_response.status_code, 200)
                self.assertContains(detail_response, 'Snapshot full content')
        finally:
            shutil.rmtree(snapshot_dir, ignore_errors=True)
            shutil.rmtree(media_root, ignore_errors=True)
            shutil.rmtree(mirror_root, ignore_errors=True)
