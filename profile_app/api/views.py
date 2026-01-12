from .serializers  import DetailProfileSerializer, BusinessProfileSeralizer, CustomerProfileSeralizer
from rest_framework import generics 
from profile_app.models import Profile
from auth_app.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permission import IsOwnerOrReadOnly

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a user profile.

    Purpose:
        - Allows users to view, edit, or delete their own profile.
        - Uses `DetailProfileSerializer` for full profile information.
        - Ensures only the profile owner can modify or delete the profile.

    Permissions:
        - IsAuthenticated: User must be logged in.
        - IsOwnerOrReadOnly: Only the owner can update or delete; others have read-only access.

    """
    serializer_class = DetailProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]



class BusinessDetailView(generics.ListAPIView):
    """
    API endpoint to list all business user profiles.

    Purpose:
        - Provides a list of all profiles belonging to business users.
        - Uses `BusinessProfileSeralizer` to format the response.

    Permissions:
        - IsAuthenticated: Only logged-in users can access this endpoint.

    Queryset:
        - Filters profiles where the related user's type is 'business'.
    """
    serializer_class = BusinessProfileSeralizer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.filter(user__type=User.UserType.business)

class CustomerDetailView(generics.ListAPIView):
    """
    API endpoint to list all customer user profiles.

    Purpose:
        - Provides a list of all profiles belonging to customer users.
        - Uses `CustomerProfileSeralizer` to format the response.

    Permissions:
        - IsAuthenticated: Only logged-in users can access this endpoint.

    Queryset:
        - Filters profiles where the related user's type is 'customer'.

    """
    serializer_class = CustomerProfileSeralizer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.filter(user__type=User.UserType.customer)    
