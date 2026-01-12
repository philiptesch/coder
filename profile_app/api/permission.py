from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class IsOwnerOrReadOnly(BasePermission):
    """
    Permission class that allows full access only to the object owner,
    while allowing read-only access to other authenticated users.

    Permissions:
        - Global permission: Any authenticated user can access the view.
        - Object-level permission:
            - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for any authenticated user.
            - Other methods (PUT, PATCH, DELETE) are only allowed for the owner of the object.

    Usage:
        - Useful for endpoints where users can view all objects but modify only their own.
        - Commonly applied to user-generated content such as posts, offers, or profiles.
    """
    def has_permission(self, request, view):
          return bool(request.user)


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user