from django.shortcuts import render
from rest_framework import generics
from register.serializers import RegisterSerializer
import rest_framework.permissions as permission_set


class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permission_set.AllowAny]

    def post(self, request, *args, **kwargs):
        super().post(request)
