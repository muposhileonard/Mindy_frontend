from rest_framework import serializers
from feed.models import Post

class PostAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'views_count',
            'reactions_count',
            'reaction_summary',
            'saves_count',
            'shares_count',
            'created_at',
        ]
