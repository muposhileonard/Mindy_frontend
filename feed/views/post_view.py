from rest_framework import viewsets, permissions
from feed.models import Post
from feed.serializers.post_serializer import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.save(created_by=self.request.user)

        # Auto-flag logic (optional)
        if post.text and "kill" in post.text.lower():  # example
            post.auto_hidden = True
            post.flagged = True
            post.save()

        # Transcript extraction (if video & empty transcript)
        if post.video and not post.transcript:
            try:
                from feed.utils.transcript import generate_transcript
                post.transcript = generate_transcript(post.video.path)
                post.save()
            except Exception as e:
                print("Transcript error:", e)
