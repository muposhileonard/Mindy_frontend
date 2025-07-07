from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from feed.models import CommentReply
from feed.serializers.comment_reply_serializer import CommentReplySerializer

class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
