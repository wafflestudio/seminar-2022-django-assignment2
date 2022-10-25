# 회원을 글을 작성할 수 있도록 해야 함. -> rest_framework.permissions.IsAuthenticated 활용하자
# Update와 Destroy는 작성자만 할 수 있도록
from rest_framework import permissions

from .models import Comment

class IsWriter(permissions.BasePermission):
    message = "You're not writer of this comment."

    def has_permission(self, request, view, obj: Comment):
        return obj.created_by == request.user