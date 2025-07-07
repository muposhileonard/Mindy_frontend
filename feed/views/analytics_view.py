from rest_framework import generics, permissions
from feed.models import Post
from feed.serializers.analytics_serializer import PostAnalyticsSerializer

class PostAnalyticsView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    
