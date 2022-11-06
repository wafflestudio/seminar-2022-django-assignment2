from rest_framework import permissions

from .models import Post

#authentication의 절차 필요 -> 어디에? rest_framework.permissions의 IsAuthenticated 활용하면 가능할 듯
class IsCreatorOrReadOnly(permissions.BasePermission):
    message = "Because current account is not writer, you don't have permission."

    # retrieve와 update시의 serializer의 obj가 다름 - 하나는 queryset, 하나는 Post
    def has_object_permission(self, request, view, obj:Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.created_by == request.user

