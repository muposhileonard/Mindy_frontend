from rest_framework import serializers
from feed.models import CommentReply

class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = ['id', 'comment', 'user', 'content', 'audio_file', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

        
