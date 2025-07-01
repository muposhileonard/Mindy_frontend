from rest_framework import serializers
from .models import MindyUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindyUser
        fields = ['contact', 'password', 'special_word']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return MindyUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    contact = serializers.CharField()
    password = serializers.CharField()
