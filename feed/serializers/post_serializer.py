from rest_framework import serializers
from feed.models import Post
from feed.utils.reactions import get_emoji_reaction_summary

def get_queryset(self):
    user = self.request.user
    if user.is_staff:
        return Post.objects.all()
    return Post.objects.filter(auto_hidden=False)


    if post.auto_hidden:
        return {
            "id": post.id,
            "status": "Hidden due to potential violation",
            "flagged": True
        }
class PostSerializer(serializers.ModelSerializer):
    reactions_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    saves_count = serializers.SerializerMethodField()
    reaction_summary = serializers.SerializerMethodField()
    class Meta:
        read_only_fields = ['created_by','transcript', 'auto_hidden', 'flagged', 'created_at', 'updated_at']
        model = Post
        fields = '__all__'

    def get_reactions_count(self, obj):
        return obj.reactions.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_reposts_count(self, obj):
        return obj.reposts.count()

    def get_saves_count(self, obj):
        return obj.saved_by.count()

    
    def get_reaction_summary(self, obj):
        reactions = obj.reactions.values_list('type', flat=True)
        count = Counter(reactions)
        return dict(count)
        return {REACTION_ICONS.get(k, k): v for k, v in count.items()}

    def get_reaction_summary(self, obj):
        return get_emoji_reaction_summary(obj.reactions.all())




        
