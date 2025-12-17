from .serializers  import DetailProfileSerializer
from rest_framework import generics 
from profile_app.models import Profile
from auth_app.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permission import IsOwnerOrReadOnly

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
