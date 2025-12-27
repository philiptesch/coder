from pyexpat import features
from urllib import request
from rest_framework import generics 
from profile_app.models import Profile
from auth_app.models import User
from coder_app.models import offers, OfferDetails
from rest_framework.views import APIView
from .seralizers  import OfferSeralizer, DetailOfferSeralizer, OfferCreateSeralizer, OfferDetailSeralizer, OfferDetailRetrieveSeralizer, OfferDetailUpdateSeralizer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permission import IsBusinessUser, IsOwnerFromOfffer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django.shortcuts import get_object_or_404

class OfferListView(APIView):
    permission_classes = [IsBusinessUser, IsAuthenticated]

    def get(self, request, format=None):
        offers_queryset = offers.objects.all()
        serializer = OfferSeralizer(offers_queryset, many=True, context={'request': request})
        return Response(serializer.data)
    

    def post(self, request, format=None):
        serializer = OfferCreateSeralizer(data=request.data, context={'request': request})

        if not request.user.is_authenticated: 
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.type != 'business':
            return Response({'detail': 'Only business users can create offers.'}, status=status.HTTP_403_FORBIDDEN)
        
        details = request.data.get('details', [])  # Immer request.data benutzen

        for detail in details:
            features = detail.get('features', [])
    
    # Prüfen, dass alle Features Strings sind
        for feature in features:
            if isinstance(feature, int):
                return Response(
                {"error": "Features dürfen keine Zahlen enthalten"},
                status=400
            )
    
        print("Features:", features)


        if serializer.is_valid():
            serializer.save(user=request.user)
            print("OFFER CREATED:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = offers.objects.all()
    serializer_class = OfferDetailSeralizer
    permission_classes = [IsOwnerFromOfffer, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        offer = self.get_object()
        serializer = self.get_serializer(offer, context={'request': request})
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return OfferDetailUpdateSeralizer
        return OfferDetailSeralizer
        
        
class OfferDetailRetrieveView(RetrieveAPIView):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailRetrieveSeralizer
    permission_classes = [AllowAny]