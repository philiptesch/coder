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
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import FilterSet, NumberFilter, DjangoFilterBackend
from rest_framework import filters
from django.db.models import Min, Max
from rest_framework.exceptions import PermissionDenied, ValidationError
class OfferListPaginatuion(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class OfferFilterSet(FilterSet):

    creator_id = NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = offers
        fields = ['creator_id']


class OfferListView(ListCreateAPIView):
    permission_classes = [IsBusinessUser, IsAuthenticated]
    pagination_class = OfferListPaginatuion
    queryset = offers.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilterSet
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSeralizer
        return OfferSeralizer

    def get_queryset(self):
        queryset= offers.objects.all()

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        min_price = self.request.query_params.get('min_price')

        queryset = queryset.annotate(max_delivery_time=Max('details__delivery_time'), min_price=Min('details__price'))

        if max_delivery_time is not None:
            try:
                max_delivery_time = int(max_delivery_time)
            except ValueError:
                raise ValidationError("max_delivery_time must be an integer.")
            queryset = queryset.filter(max_delivery_time__lte=max_delivery_time)

        if min_price is not None:
            try:
                 min_price = float(min_price.replace(',', '.'))
            except ValueError:
                raise ValidationError({"min_price": "Must be a number."})
            queryset = queryset.filter(min_price__gte=min_price)

        return queryset

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

