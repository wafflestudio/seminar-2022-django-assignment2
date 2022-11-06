from rest_framework.pagination import CursorPagination


class PostPagination(CursorPagination):
    page_size = 5
    ordering = '-created_at'


class CommentPagination(CursorPagination):
    page_size = 30
    ordering = 'created_at'


class TagPagination(CursorPagination):
    page_size = 30
    ordering = 'created_at'
