from django.shortcuts import render
from rest_framework import generics

from register.permissions import IsAdminOrAnonymous, IsAdminOrUser
from register.serializers import RegisterSerializer, TokenSerializer
import rest_framework.permissions as permission_set
from rest_framework.authtoken.models import Token


class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminOrAnonymous]


class GetTokenAPI(generics.RetrieveAPIView):
    serializer_class = TokenSerializer
    permission_classes = [IsAdminOrUser]
    lookup_field = 'user_id'

    def get_queryset(self):
        return Token.objects.filter(user_id=self.kwargs['user_id'])

