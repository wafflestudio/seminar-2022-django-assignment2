from rest_framework.pagination import CursorPagination


class BlogCursorPagination(CursorPagination):
    ordering = '-created_at'
