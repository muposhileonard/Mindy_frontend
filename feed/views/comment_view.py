from rest_framework import viewsets
from feed.models import Comment
from feed.serializers.comment_serializer import CommentSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    parser_classes = [MultiPartParser, FormParser]  # Enable file upload

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'detail': 'You can only delete your own comments.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        if not post.allow_comments:
            raise PermissionDenied("Comments are turned off for this post.")
        serializer.save(user=self.request.user)
