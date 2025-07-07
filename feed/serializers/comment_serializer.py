from rest_framework import serializers
from feed.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'voice_note', 'created_at']

        
