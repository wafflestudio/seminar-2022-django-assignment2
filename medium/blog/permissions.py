from rest_framework.permissions import IsAdminUser, SAFE_METHODS

class IsOwnerOrReadOnly(IsAdminUser):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the user who create the post, comments.E
        return obj.author == request.user
