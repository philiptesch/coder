from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.type == 'business')
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user.is_authenticated and request.user.type == 'business':
                return True
            
class IsOwnerFromOfffer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if  request.user.is_authenticated and  request.method in  ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user

