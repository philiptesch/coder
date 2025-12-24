from rest_framework import generics 
from profile_app.models import Profile
from auth_app.models import User
from coder_app.models import offers
from .seralizers  import OfferSeralizer, DetailOfferSeralizer
from rest_framework.permissions import IsAuthenticated, AllowAny


class OfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSeralizer
    queryset = offers.objects.all()
    permission_classes = [AllowAny]