from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import SignUpSerializer, LogInSerializer


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"msg": "user created"}
        return JsonResponse(data, status=status.HTTP_201_CREATED)


#
# class LoginView(generics.GenericAPIView):
#
#     def post(self, request):
#         user = authenticate(username=request.data['username'], password=request.data['password'])
#         if user is not None:
#             token = Token.objects.get(user=user)
#             return Response({"Token": token.key})
#         else:
#             return Response(status=401)

class LogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
