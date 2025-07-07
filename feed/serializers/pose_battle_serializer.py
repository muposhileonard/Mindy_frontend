# feed/serializers/pose_battle_serializer.py

from rest_framework import serializers
from feed.models import PoseBattleEntry

class PoseBattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoseBattleEntry
        fields = '__all__'
        read_only_fields = ['accepted', 'denied', 'voted_users', 'challenger_votes', 'opponent_votes']

        
