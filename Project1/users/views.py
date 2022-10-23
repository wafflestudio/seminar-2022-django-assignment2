from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import FileUploadParser
from users.models import User, UserFollowing
from users.serializers import UserSerializer, FollowingSerializer, FollowersSerializer

# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FileUploadParser)
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserFollowingView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    queryset = UserFollowing.objects.all()

class UserFollowersView(generics.ListAPIView):
    serializer_class = FollowersSerializer

    def get_queryset(self):
        # 현재 접속한 user 말고 다른 user를 알아오는 방법은 없을까? -> request에서 url을 따오는 방법
        # url의 경우, serializer에 SerializerMethodField로 설정하고 get_field 메소드 정의하여 갖고올 수 있다...
        user = self.request.user
        return user.followers.all()



class UserProfilePhotoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    parser_classes = (FileUploadParser)
    permission_classes = [IsAuthenticatedOrReadOnly]
