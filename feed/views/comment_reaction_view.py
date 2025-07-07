from rest_framework import viewsets
from feed.models import CommentReaction
from feed.serializers.comment_reaction_serializer import CommentReactionSerializer
from rest_framework.permissions import IsAuthenticated

class CommentReactionViewSet(viewsets.ModelViewSet):
    queryset = CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        existing = CommentReaction.objects.filter(
            user=self.request.user,
            comment=serializer.validated_data['comment']
        ).first()
        if existing:
            existing.delete()  # toggle off if exists
        else:
            serializer.save(user=self.request.user)
