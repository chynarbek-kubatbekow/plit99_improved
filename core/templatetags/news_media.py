from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


NEWS_STATIC_COVERS = {
    'alatoo-hub-battle': 'img/news-covers/news-alatoo-hub-battle.jpg',
    'chinese-certificates': 'img/news-covers/news-chinese-certificates.jpg',
    'techwomen-volunteers': 'img/news-covers/news-techwomen-volunteers.jpg',
    'ai-summit-april-1': 'img/news-covers/news-ai-summit-april-1.jpg',
    'c306681c': 'img/news-covers/news-chinese-cooking-masterclass.jpg',
    '3b871fdd': 'img/news-covers/news-career-orientation.jpg',
    '7da9f42f': 'img/news-covers/news-sarmerden-nooruz.jpg',
    'no99-21': 'img/news-covers/news-school-21.jpg',
    '2-3': 'img/news-covers/news-german-hackathon.jpg',
}


def safe_static_url(path):
    try:
        return static(path)
    except ValueError:
        base_url = getattr(settings, 'STATIC_URL', '/static/')
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


@register.filter
def news_static_cover(news):
    cover_image = getattr(news, 'cover_image', None)
    if cover_image and getattr(cover_image, 'name', ''):
        try:
            return cover_image.url
        except (OSError, ValueError):
            pass

    slug = getattr(news, 'slug', '')
    path = NEWS_STATIC_COVERS.get(slug)
    return safe_static_url(path) if path else ''
