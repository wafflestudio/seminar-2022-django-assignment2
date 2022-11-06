from rest_framework.pagination import CursorPagination


class PostPagination(CursorPagination):
    ordering = '-created_at'
    page_size = 10


class CommentPagination(CursorPagination):
    ordering = '-created_at'
    page_size = 10


class TagPagination(CursorPagination):
    ordering = 'content'
    page_size = 10
