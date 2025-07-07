from rest_framework import serializers
from feed.models import CommentReaction

class CommentReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReaction
        fields = ['id', 'user', 'comment', 'reaction_type', 'created_at']
        read_only_fields = ['id', 'created_at']
