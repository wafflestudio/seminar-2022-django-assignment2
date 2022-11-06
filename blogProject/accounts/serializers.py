from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LogInSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'token': user.tokens()['token']
        }

    class Meta:
        model = User
        fields = ['password', 'username', 'tokens', ]

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('user not active')

        return {
            'username': user.username,
            'tokens': user.tokens
        }
