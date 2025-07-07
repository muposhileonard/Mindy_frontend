# feed/serializers/bookmark_serializer.py

from rest_framework import serializers
from feed.models import PostBookmark

class PostBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBookmark
        fields = ['id', 'post', 'created_at']
        read_only_fields = ['id', 'created_at']
