from rest_framework.pagination import CursorPagination


class PostListPagination(CursorPagination):
    page_size = 15
    ordering = '-created_at'


class CommentListPagination(CursorPagination):
    page_size = 30
    ordering = '-created_at'
