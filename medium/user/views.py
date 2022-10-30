from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views
from rest_framework.authtoken import models as token_models

from user import serializers as user_serializers


class SignUpView(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = user_serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = token_models.Token.objects.create(user=user)
        serializer.data["Token"] = token
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LoginView(views.APIView):
    def post(self, request):
        user = auth.authenticate(**request.data)

        if user is not None:
            token = token_models.Token.objects.get(user=user)
            return response.Response({"Token": token.key})
        else:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
