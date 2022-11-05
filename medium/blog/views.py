from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, PostListSerializer

from django.contrib.auth import authenticate, hashers
from django.contrib.auth.models import User

from rest_framework import generics, permissions, decorators
from rest_framework import viewsets, mixins,status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('login', request=request, format=format),
        'logout': reverse('logout', request=request, format=format),
        'register': reverse('register', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
    })


@api_view(['GET', 'POST'])
@decorators.permission_classes((permissions.AllowAny,))
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)


@decorators.authentication_classes([TokenAuthentication])
@decorators.permission_classes([IsOwnerOrReadOnly, permissions.IsAdminUser])
def logout(request):
    request.user.token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@decorators.permission_classes((permissions.AllowAny,))
def register(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        fullname = request.data.get('fullname')

        user = User.objects.create_user(email=email, password=hashers.make_password(password), full_name=fullname)
        if user:
            return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_417_EXPECTATION_FAILED)


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all().defer('description')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    # Token authentication
    elif request.method == 'POST':
        return post_create(request)


@decorators.authentication_classes([TokenAuthentication])
@decorators.permission_classes([IsOwnerOrReadOnly, permissions.IsAdminUser])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSets(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    authentication_classes = [TokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAdminUser]


class CommentListAPI(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
def post_comment_list(request, pk):
    if request.method == 'GET':
        posts = Comment.objects.filter(post__id=pk)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


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