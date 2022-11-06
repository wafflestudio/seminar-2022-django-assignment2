from rest_framework.permissions import BasePermission, SAFE_METHODS

from blog.models import Post


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return view.kwargs['pk'] == request.user.id


class IsObjectOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by.id == request.user.id
