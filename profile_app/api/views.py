from .serializers  import DetailProfileSerializer, BusinessProfileSeralizer, CustomerProfileSeralizer
from rest_framework import generics 
from profile_app.models import Profile
from auth_app.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permission import IsOwnerOrReadOnly

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]



class BusinessDetailView(generics.ListAPIView):
    serializer_class = BusinessProfileSeralizer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.filter(user__type=User.UserType.business)

class CustomerDetailView(generics.ListAPIView):
    serializer_class = CustomerProfileSeralizer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.filter(user__type=User.UserType.customer)    
