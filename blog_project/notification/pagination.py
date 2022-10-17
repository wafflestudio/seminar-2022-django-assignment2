from rest_framework.pagination import CursorPagination
from .models import Notification


class NotificationPagination(CursorPagination):
    page_size = 30
    ordering = '-created_at'
