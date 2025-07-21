from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

#  Serializers for User model and authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['__all__']  # Include all fields from the User model

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['__all__']  # Include all fields from the User model
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            profile_picture=validated_data.get('profile_picture'),
            bio=validated_data.get('bio', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")