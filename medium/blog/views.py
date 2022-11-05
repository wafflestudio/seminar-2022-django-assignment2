from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, PostListSerializer


from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'preview_posts': reverse('post-list', request=request, format=format),
        'posts' : reverse('post-create', request=request, format=format),
        'preview_comments': reverse('comment-list', request=request, format=format),
        'comments': reverse('comment-create', request=request, format=format),
    })

class PostListAPI(generics.ListAPIView):
    queryset = Post.objects.all().defer('description')
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]


class PostViewSets(viewsets.mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    authentication_classes = [TokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentListAPI(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]


class CommentViewSets(viewsets.mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    authentication_classes = [TokenAuthentication]
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(is_updated=True)