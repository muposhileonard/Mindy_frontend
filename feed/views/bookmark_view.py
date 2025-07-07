from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, permissions
from feed.models import PostBookmark
from feed.serializers.bookmark_serializer import PostBookmarkSerializer

class PostBookmarkViewSet(viewsets.ModelViewSet):
    queryset = PostBookmark.objects.all()
    serializer_class = PostBookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PostBookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
