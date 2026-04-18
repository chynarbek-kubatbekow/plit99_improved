from django.shortcuts import render, get_object_or_404
from .models import News, NewsCategory, GalleryItem, GalleryCategory


def index(request):
    featured_news = News.objects.filter(is_published=True, is_featured=True).first()
    latest_news   = News.objects.filter(is_published=True).exclude(
        pk=featured_news.pk if featured_news else 0
    )[:3]
    return render(request, 'core/index.html', {
        'featured_news': featured_news,
        'latest_news': latest_news,
    })


def about(request):
    return render(request, 'core/about.html')


def education(request):
    return render(request, 'core/education.html')


def results(request):
    return render(request, 'core/results.html')


def admission(request):
    return render(request, 'core/admission.html')


def media_hub(request):
    view_mode = request.GET.get('view', 'all')
    if view_mode not in {'all', 'news', 'gallery'}:
        view_mode = 'all'

    news_categories = NewsCategory.objects.all()
    gallery_categories = GalleryCategory.objects.all()

    news_qs = News.objects.filter(is_published=True)
    news_cat_slug = request.GET.get('news_cat')
    active_news_cat = None
    if news_cat_slug:
        active_news_cat = get_object_or_404(NewsCategory, slug=news_cat_slug)
        news_qs = news_qs.filter(category=active_news_cat)

    featured = news_qs.filter(is_featured=True).first()
    news_list = news_qs.exclude(pk=featured.pk if featured else 0)

    gallery_qs = GalleryItem.objects.filter(is_published=True)
    gallery_cat_slug = request.GET.get('gallery_cat')
    active_gallery_cat = None
    if gallery_cat_slug:
        active_gallery_cat = get_object_or_404(GalleryCategory, slug=gallery_cat_slug)
        gallery_qs = gallery_qs.filter(category=active_gallery_cat)

    return render(request, 'core/media_hub.html', {
        'view_mode': view_mode,
        'news_categories': news_categories,
        'gallery_categories': gallery_categories,
        'active_news_cat': active_news_cat,
        'active_gallery_cat': active_gallery_cat,
        'featured': featured,
        'news_list': news_list,
        'gallery_items': gallery_qs,
    })


def news_list(request):
    category_slug = request.GET.get('cat')
    categories    = NewsCategory.objects.all()
    news_qs       = News.objects.filter(is_published=True)

    active_cat = None
    if category_slug:
        active_cat = get_object_or_404(NewsCategory, slug=category_slug)
        news_qs    = news_qs.filter(category=active_cat)

    featured = news_qs.filter(is_featured=True).first()
    news_qs  = news_qs.exclude(pk=featured.pk if featured else 0)

    return render(request, 'core/news.html', {
        'news_list': news_qs,
        'featured':  featured,
        'categories': categories,
        'active_cat': active_cat,
    })


def news_detail(request, slug):
    news    = get_object_or_404(News, slug=slug, is_published=True)
    related = News.objects.filter(is_published=True).exclude(pk=news.pk)[:3]
    return render(request, 'core/news_detail.html', {'news': news, 'related': related})


def gallery(request):
    category_slug = request.GET.get('cat')
    categories    = GalleryCategory.objects.all()
    items_qs      = GalleryItem.objects.filter(is_published=True)

    active_cat = None
    if category_slug:
        active_cat = get_object_or_404(GalleryCategory, slug=category_slug)
        items_qs   = items_qs.filter(category=active_cat)

    return render(request, 'core/gallery.html', {
        'items': items_qs,
        'categories': categories,
        'active_cat': active_cat,
    })


def contacts(request):
    return render(request, 'core/contacts.html')
