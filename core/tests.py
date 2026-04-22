import shutil
import uuid
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
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
                    'large-news-cover.JPG',
                    build_test_image(),
                    content_type='image/jpeg',
                )
                news = News.objects.create(
                    title='Test news',
                    excerpt='Short excerpt',
                    content='Full text',
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

    def test_news_detail_renders_escaped_html_content_as_real_paragraphs(self):
        news = News.objects.create(
            title='Escaped HTML content news',
            slug='escaped-html-content-news',
            excerpt='Short excerpt',
            content='&lt;p&gt;Paragraph from database.&lt;/p&gt;',
        )

        with self.settings(SECURE_SSL_REDIRECT=False):
            response = self.client.get(f'/news/{news.slug}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>Paragraph from database.</p>', html=False)
        self.assertNotContains(response, '&lt;p&gt;Paragraph from database.&lt;/p&gt;', html=False)

    def test_news_detail_renders_double_escaped_html_content_as_real_paragraphs(self):
        news = News.objects.create(
            title='Double escaped HTML content news',
            slug='double-escaped-html-content-news',
            excerpt='Short excerpt',
            content='&amp;lt;p&amp;gt;Double escaped paragraph.&amp;lt;/p&amp;gt;',
        )

        with self.settings(SECURE_SSL_REDIRECT=False):
            response = self.client.get(f'/news/{news.slug}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>Double escaped paragraph.</p>', html=False)
        self.assertNotContains(
            response,
            '&amp;lt;p&amp;gt;Double escaped paragraph.&amp;lt;/p&amp;gt;',
            html=False,
        )
