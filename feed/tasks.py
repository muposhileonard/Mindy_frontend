# feed/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from feed.models import PostBookmark

@shared_task
def delete_expired_bookmarks():
    cutoff = timezone.now() - timedelta(days=7)
    deleted, _ = PostBookmark.objects.filter(created_at__lt=cutoff).delete()
    return f"Deleted {deleted} expired bookmarks"
