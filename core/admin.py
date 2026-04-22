from django.contrib import admin

from .models import GalleryCategory, GalleryItem, News, NewsCategory


admin.site.register(NewsCategory)
admin.site.register(News)
admin.site.register(GalleryCategory)
admin.site.register(GalleryItem)
