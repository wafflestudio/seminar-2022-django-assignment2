from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import FileUploadParser
from users.models import User, UserFollowing
from users.serializers import UserSerializer, FollowingSerializer, FollowersSerializer
from users.permissions import IsSuperUser, IsAccountOwner
from posts.serializers import PostListSerializer
# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FileUploadParser)
    permission_classes = [IsSuperUser]
    def get_exception_handler(self):


#본인이거나 superuser가 아니라면 유저에 대한 정보 열람, 수정, 삭제 안되게...
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser | IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_exception_handler(self):

class UserFollowingView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    queryset = UserFollowing.objects.all()

    def get_exception_handler(self):

class UserFollowersView(generics.ListAPIView):
    serializer_class = FollowersSerializer
    def get_queryset(self):
        # 현재 접속한 user 말고 다른 user를 알아오는 방법은 없을까? -> request에서 url을 따오는 방법
        # url의 경우, serializer에 SerializerMethodField로 설정하고 get_field 메소드 정의하여 갖고올 수 있다...
        user = self.request.user
        return user.followers.all()
    def get_exception_handler(self):

class UserProfilePhotoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    parser_classes = (FileUploadParser)
    permission_classes = [IsAccountOwner]
    def get_exception_handler(self):

# user post list 필요
class UserPostListView(generics.ListAPIView):
    # 앞에 300자만 가져와야 함 + user 정보를 받아서 해당 user의 게시글을 받아와야 함.
    # request를 보낸 user가 아니라
    # 기존에 제네릭 뷰와는 달리 Post 클래스의 created_by를 통해서 가지고 와야 함.
    serializer_class = PostListSerializer
    def get_queryset(self):
        user = self.request.user
        return user.posts.all()
    def get_exception_handler(self):
