
# feed/views/save_view.py

from rest_framework import viewsets, permissions
from feed.models import PostSave
from feed.serializers.save_serializer import PostSaveSerializer

class PostSaveViewSet(viewsets.ModelViewSet):
    queryset = PostSave.objects.all()
    serializer_class = PostSaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PostSave.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
