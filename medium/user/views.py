from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created",
                "data": serializer.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request: Request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            response = {
                "message": "Login Successful",
                "token": user.auth_token.key,
            }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }

        return Response(data=content, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get(self, request: Request):

        user = request.user

        serializer = self.serializer_class(user, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)
