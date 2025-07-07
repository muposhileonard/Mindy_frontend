# feed/serializers/repost_serializer.py

from rest_framework import serializers
from feed.models import Repost

class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repost
        fields = ['id', 'original_post', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']
