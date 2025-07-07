from rest_framework import viewsets
from feed.models import Comment
from feed.serializers.comment_serializer import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
