from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    ordering = '-created_by'
    page_size = 10
