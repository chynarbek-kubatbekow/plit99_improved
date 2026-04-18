from unittest.mock import patch

from django.db import OperationalError
from django.test import TestCase


class PublicPagesResilienceTests(TestCase):
    def test_media_hub_falls_back_when_database_is_unavailable(self):
        with self.settings(SECURE_SSL_REDIRECT=False):
            with patch('core.views.NewsCategory.objects.all', side_effect=OperationalError('db is down')):
                response = self.client.get('/media/')

        self.assertEqual(response.status_code, 200)

    def test_gallery_page_falls_back_when_database_is_unavailable(self):
        with self.settings(SECURE_SSL_REDIRECT=False):
            with patch('core.views.GalleryCategory.objects.all', side_effect=OperationalError('db is down')):
                response = self.client.get('/gallery/')

        self.assertEqual(response.status_code, 200)
