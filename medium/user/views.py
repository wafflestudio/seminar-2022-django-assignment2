from django.contrib.auth.models import User
from rest_framework import generics, permissions
from user import serializers as user_serializers


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = user_serializers.RegisterSerializer
