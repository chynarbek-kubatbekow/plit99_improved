from django import template
from django.templatetags.static import static

from core.media_utils import stored_media_exists

register = template.Library()


NEWS_STATIC_COVERS = {
    '3b871fdd': 'img/news-covers/news-career-orientation.jpg',
    '7da9f42f': 'img/news-covers/news-sarmerden-nooruz.jpg',
    'no99-21': 'img/news-covers/news-school-21.jpg',
    '2-3': 'img/news-covers/news-german-hackathon.jpg',
}


@register.filter
def news_static_cover(news):
    cover_image = getattr(news, 'cover_image', None)
    if cover_image and getattr(cover_image, 'name', ''):
        try:
            if stored_media_exists(cover_image.name):
                return cover_image.url
        except OSError:
            pass

    slug = getattr(news, 'slug', '')
    path = NEWS_STATIC_COVERS.get(slug)
    return static(path) if path else ''
