from rest_framework.pagination import CursorPagination
from .models import Post, Comment, Tag


class PostPagination(CursorPagination):
    page_size = 30
    ordering = '-created_at'


class CommentPagination(CursorPagination):
    page_size = 30
    ordering = 'created_at'


class TagPagination(CursorPagination):
    page_size = 30
    ordering = 'created_at'
