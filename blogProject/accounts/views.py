from django.http import JsonResponse
from rest_framework import generics, status
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


class LogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
