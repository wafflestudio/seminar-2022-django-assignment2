from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import User
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'password',
            'nickname',
            'short_bio',
            'photo',
            'url',
            'followers',
            'following'
        )
        extra_kwargs = {'password': {'write_only': True}}
        model = User

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            nickname=validated_data.get('nickname'),
            short_bio=validated_data.get('short_bio'),
            photo=validated_data.get('photo'),
            url=validated_data.get('url')
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
