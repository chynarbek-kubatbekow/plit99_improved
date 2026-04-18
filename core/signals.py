import logging

from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .content_snapshot import safe_export_content_snapshot
from .models import GalleryCategory, GalleryItem, News, NewsCategory


logger = logging.getLogger(__name__)


def _schedule_snapshot_refresh():
    try:
        transaction.on_commit(safe_export_content_snapshot)
    except RuntimeError:
        safe_export_content_snapshot()


@receiver(post_save, sender=NewsCategory)
@receiver(post_save, sender=News)
@receiver(post_save, sender=GalleryCategory)
@receiver(post_save, sender=GalleryItem)
def refresh_snapshot_after_save(sender, instance, raw=False, **kwargs):
    if raw:
        return
    _schedule_snapshot_refresh()


@receiver(post_delete, sender=NewsCategory)
@receiver(post_delete, sender=News)
@receiver(post_delete, sender=GalleryCategory)
@receiver(post_delete, sender=GalleryItem)
def refresh_snapshot_after_delete(sender, instance, **kwargs):
    _schedule_snapshot_refresh()
