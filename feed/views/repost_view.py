from rest_framework import viewsets, permissions
from feed.models import Repost
from feed.serializers.repost_serializer import RepostSerializer

class RepostViewSet(viewsets.ModelViewSet):
    queryset = Repost.objects.all()
    serializer_class = RepostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Repost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
