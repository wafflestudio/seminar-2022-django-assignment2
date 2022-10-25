from django.shortcuts import render

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from models import Comment
from serializers import CommentSerializer
from permissions import IsWriter
# Create your views here.
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_exception_handler(self):
class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_exception_handler(self):
class CommentUpdateDestoryView(generics.GenericAPIView,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin):
    permission_classes = [IsWriter | IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_exception_handler(self):