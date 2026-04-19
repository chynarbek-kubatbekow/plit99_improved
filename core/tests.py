from io import BytesIO
from pathlib import Path
import shutil
import uuid
from unittest.mock import patch

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import OperationalError
from django.test import TestCase
from PIL import Image

from .models import News


def build_test_image(width=2600, height=1800, color=(20, 80, 160)):
    image = Image.new('RGB', (width, height), color=color)
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=95)
    return buffer.getvalue()


def make_workspace_media_root():
    path = Path(settings.BASE_DIR) / '.test-media' / uuid.uuid4().hex
    path.mkdir(parents=True, exist_ok=True)
    return path


class NewsMediaTests(TestCase):
    def test_news_cover_upload_is_resized_and_saved_to_safe_path(self):
        media_root = make_workspace_media_root()
        try:
            with self.settings(MEDIA_ROOT=media_root, SERVE_MEDIA_FILES=True):
                upload = SimpleUploadedFile(
                    'Большое Фото Для Новости.JPG',
                    build_test_image(),
                    content_type='image/jpeg',
                )
                news = News.objects.create(
                    title='Тестовая новость',
                    excerpt='Короткое описание',
                    content='Полный текст новости',
                    cover_image=upload,
                )

                self.assertTrue(news.cover_image.name.startswith('news/covers/'))
                self.assertTrue(news.cover_image.name.endswith('.jpg'))

                with Image.open(news.cover_image.path) as saved_image:
                    self.assertLessEqual(saved_image.width, 1600)
                    self.assertLessEqual(saved_image.height, 1600)
        finally:
            shutil.rmtree(media_root, ignore_errors=True)

    def test_media_files_are_served_with_cache_headers(self):
        media_root = make_workspace_media_root()
        try:
            with self.settings(MEDIA_ROOT=media_root, SERVE_MEDIA_FILES=True, SECURE_SSL_REDIRECT=False):
                media_file = media_root / 'news' / 'covers' / 'cached.jpg'
                media_file.parent.mkdir(parents=True, exist_ok=True)
                media_file.write_bytes(build_test_image(width=600, height=400))

                response = self.client.get('/media/news/covers/cached.jpg')

                self.assertEqual(response.status_code, 200)
                self.assertIn('max-age=', response['Cache-Control'])
                self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        finally:
            shutil.rmtree(media_root, ignore_errors=True)

    def test_home_page_falls_back_when_database_is_unavailable(self):
        with self.settings(SECURE_SSL_REDIRECT=False):
            with patch('core.views.News.objects.filter', side_effect=OperationalError('db is down')):
                response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<!DOCTYPE html>', html=False)

    def test_news_page_falls_back_when_database_is_unavailable(self):
        with self.settings(SECURE_SSL_REDIRECT=False):
            with patch('core.views.NewsCategory.objects.all', side_effect=OperationalError('db is down')):
                response = self.client.get('/news/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новости')
    def test_news_detail_renders_html_content_without_escaped_paragraph_tags(self):
        news = News.objects.create(
            title='HTML content news',
            slug='html-content-news',
            excerpt='Short excerpt',
            content='<p>First paragraph.</p><p>Second paragraph.</p>',
        )

        with self.settings(SECURE_SSL_REDIRECT=False):
            response = self.client.get(f'/news/{news.slug}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>First paragraph.</p>', html=False)
        self.assertNotContains(response, '&lt;p&gt;First paragraph.&lt;/p&gt;', html=False)
