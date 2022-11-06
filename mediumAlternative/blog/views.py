from rest_framework import mixins, generics
from rest_framework.permissions import *
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from blog.models import Post
from blog.models import Comment
from blog.permissions import *
from blog.serializers import *


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | IsPostCreator]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()

    def get(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(post_id__exact=kwargs['post_pk'])
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request, 'post_pk': kwargs['post_pk']})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateDeleteView(mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              generics.GenericAPIView):
    permission_classes = [IsAdminUser | IsCommentCreator]
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
