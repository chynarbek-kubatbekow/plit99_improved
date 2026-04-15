from django.contrib import admin
from django.utils.html import format_html
from .models import NewsCategory, News, GalleryCategory, GalleryItem

admin.site.site_header = 'ПЛИТ №99 — Панель управления'
admin.site.site_title  = 'ПЛИТ №99'
admin.site.index_title = 'Управление сайтом'


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display   = ['title', 'category', 'is_featured', 'is_published', 'published_at', 'cover_preview']
    list_filter    = ['is_published', 'is_featured', 'category', 'published_at']
    search_fields  = ['title', 'excerpt', 'content']
    list_editable  = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering       = ['-published_at']

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content')
        }),
        ('Обложка', {
            'fields': ('cover_image', 'cover_emoji', 'cover_gradient'),
            'description': 'Загрузите фото ИЛИ укажите эмодзи + градиент для заглушки'
        }),
        ('Публикация', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="height:48px;border-radius:6px;object-fit:cover"/>', obj.cover_image.url)
        return format_html('<span style="font-size:1.5rem">{}</span>', obj.cover_emoji)
    cover_preview.short_description = 'Превью'


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display  = ['__str__', 'media_type', 'category', 'is_published', 'order', 'image_preview']
    list_filter   = ['media_type', 'category', 'is_published']
    list_editable = ['is_published', 'order']
    search_fields = ['title']

    fieldsets = (
        ('Медиа', {'fields': ('media_type', 'image', 'video_url', 'title')}),
        ('Настройки', {'fields': ('category', 'is_published', 'order')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:48px;width:72px;border-radius:6px;object-fit:cover"/>', obj.image.url)
        if obj.video_url:
            return format_html('<span style="color:#1668C0">▶ Видео</span>')
        return '—'
    image_preview.short_description = 'Превью'
