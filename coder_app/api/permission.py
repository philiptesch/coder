from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView


class IsBusinessUser(BasePermission):
    """
    Permission class for business users.

    Permissions:
        - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for any authenticated business user.
        - POST requests are only allowed for authenticated business users.
        - Object-level permission: Only the business user owning the object can modify it.

    Usage:
        Typically used for endpoints where business users create or manage offers.
    """
    def has_permission(self, request, view):
            if request.method in SAFE_METHODS:
                return True
            
            if request.user.is_authenticated and request.user.type == 'business' and request.method in  ['POST']: 
                 return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user.is_authenticated and request.user.type == 'business':
                return True
            
        return obj.business_user == request.user
    

class IsBusinessAndAdminUser(BasePermission):
    """
    Permission class for business and admin users.

    Permissions:
        - Global permission: Only authenticated business users can access.
        - Object-level permission:
            - SAFE_METHODS are allowed for any authenticated business user.
            - DELETE is restricted to staff users.
            - PATCH is restricted to business users.

    Usage:
        Typically used for endpoints where business users or admins can update or delete orders.
    """
    def has_permission(self, request, view):
            return bool(request.user and request.user.is_authenticated and request.user.type == 'business')
    

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
                return True

        if request.method == 'DELETE':
           return(request.user and request.user.is_authenticated and request.user.is_staff) 

        if request.method == 'PATCH': 
            return(request.user and request.user.is_authenticated and request.user.type == 'business')


class IsCustomerUserForReviews(BasePermission):
    """
    Permission class for customer users creating or viewing reviews.

    Permissions:
        - Global permission: Any authenticated user can access the view.
        - Object-level permission:
            - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for all authenticated users.
            - POST requests are only allowed for authenticated users of type 'customer'.

    Usage:
        Used for review creation and listing endpoints.
    """

    def has_permission(self, request, view):
             if request.user.is_authenticated:
                return True
             
    def has_object_permission(self, request, view, obj):
            
            if request.user.is_authenticated and  request.method in  ['GET', 'HEAD', 'OPTIONS']:
                return True
            
            if request.user.is_authenticated and request.user.type == 'customer' and request.method in  ['POST']:
                 return True


class IsOwnerFromOfffer(BasePermission):
    """
    Permission class for owners of offers.

    Permissions:
        - Global permission: Any authenticated user can access.
        - Object-level permission:
            - SAFE_METHODS are allowed for all authenticated users.
            - Only the user who owns the offer object can modify it (PUT, PATCH, DELETE).

    Usage:
        Applied to offer detail endpoints to restrict edits to the offer creator.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if  request.user.is_authenticated and  request.method in  ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user


class IsCustomerUser(BasePermission):
    """
    Permission class for customer users managing orders.

    Permissions:
        - Global permission: Any authenticated user can access the view.
        - Object-level permission:
            - SAFE_METHODS are allowed for all authenticated users.
            - Only the customer user who owns the order can modify it.

    Usage:
        Applied to order endpoints to restrict actions to the customer.
    """

    def has_permission(self, request, view):
         if request.user.is_authenticated:
            return True
    
    def has_object_permission(self, request, view, obj):
        if  request.user.is_authenticated and  request.method in  ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.user.type == 'customer':
            return obj.customer_user == request.user
        
class isReviewer(BasePermission):
    """
    Permission class for reviewers managing their reviews.

    Permissions:
        - Global permission: Any authenticated user can access the view.
        - Object-level permission:
            - Only the user who is the reviewer of the review object can modify it.

    Usage:
        Applied to review detail endpoints to ensure only the reviewer can edit or delete their review.
    """

    def has_permission(self, request, view):
         if request.user.is_authenticated:
            return True
         
    def has_object_permission(self, request, view, obj):
         return obj.reviewer == request.user
