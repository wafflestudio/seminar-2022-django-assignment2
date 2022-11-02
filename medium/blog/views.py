from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework import views
from .permissions import IsAuthorOrReadOnly
from .serializers import *
from django.shortcuts import get_object_or_404


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostListSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            created_by = request.user
            summary = request.data['description'][:300]
            read_time = 1 + len(request.data['description']) / 100
            tag = []
            for _, tag_name in enumerate(request.data['tags']):
                tags = Tag.objects.get_or_create(tag_name=tag_name)
                # if tags.pk not in tag:
                tag.append(tags[0])
            serializer.save(created_by=created_by,
                            summary=summary,
                            read_time=read_time,
                            tag=tag)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly or permissions.IsAdminUser]

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    multiple_lookup_field = ['pk']

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_field:
            filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = CommentSerializer

    multiple_lookup_field = ['pk']

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_field:
            filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        post = self.get_object()

        serializer = CommentSerializer(data=request.data)
        if 'parent' in request.data:
            parent = request.data['parent']

            parent = get_object_or_404(Comment, pk=parent)
            if serializer.is_valid():
                serializer.save(parent=parent)

        if serializer.is_valid():
            created_by = request.user
            tag = []
            for _, tag_name in enumerate(request.data['tags']):
                tags = Tag.objects.get_or_create(tag_name=tag_name)
                # if tags.pk not in tag:
                tag.append(tags[0])
            # tag = Tag.objects.get_or_create(tag_name=request.data['tag'])
            serializer.save(created_by=created_by,
                            post=post,
                            tag=tag)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        post = self.get_object()
        comment = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comment, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthorOrReadOnly or permissions.IsAdminUser]

    serializer_class = CommentSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, post=self.kwargs['pid'], pk=self.kwargs['cid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        is_updated = True

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_updated=is_updated)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagPostListView(views.APIView):

    def get(self, request, tag_name):
        post = Post.objects.filter(tag__tag_name=tag_name)
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostListSerializer(post, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TagCommentListView(views.APIView):

    def get(self, request, tag_name):
        comment = Comment.objects.filter(tag__tag_name=tag_name)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = []
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
