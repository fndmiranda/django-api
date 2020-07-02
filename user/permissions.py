from rest_framework import permissions


class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow system superuser to edit it.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser
