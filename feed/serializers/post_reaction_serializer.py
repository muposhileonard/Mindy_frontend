def perform_create(self, serializer):
    post = serializer.validated_data['post']
    if not post.allow_reactions:
        raise PermissionDenied("Reactions are turned off for this post.")
    serializer.save(user=self.request.user)

    
