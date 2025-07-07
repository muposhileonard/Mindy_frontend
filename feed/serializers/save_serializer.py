# feed/serializers/save_serializer.py

from rest_framework import serializers
from feed.models import PostSave

class PostSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSave
        fields = ['id', 'post', 'is_bookmark', 'saved_at']
        read_only_fields = ['id', 'saved_at']

        
