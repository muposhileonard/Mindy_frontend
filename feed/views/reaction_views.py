from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from feed.models import PostReaction
from feed.serializers.reaction_serializer import PostReactionSerializer
from rest_framework.response import Response

 
class PostReactionViewSet(viewsets.ModelViewSet):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        post = serializer.validated_data['post']
        reaction_type = serializer.validated_data['reaction_type']
        serializer.save(user=self.request.user)
        
        existing = PostReaction.objects.filter(user=user, post=post).first()

        if existing:
            if existing.reaction_type == reaction_type:
                # Same reaction -> toggle (remove it)
                existing.delete()
                raise Response({"message": "Reaction removed."}, status=status.HTTP_204_NO_CONTENT)
            else:
                # Different reaction -> update it
                existing.reaction_type = reaction_type
                existing.save()
                raise Response(PostReactionSerializer(existing).data, status=status.HTTP_200_OK)
        else:
            serializer.save(user=user)
