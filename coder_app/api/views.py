from pyexpat import features
from urllib import request
from rest_framework import generics 
from profile_app.models import Profile
from auth_app.models import User
from coder_app.models import offers, OfferDetails, Orders, Review
from rest_framework.views import APIView
from .seralizers  import OfferSeralizer,OfferCreateSeralizer, OfferDetailSeralizer, OfferDetailRetrieveSeralizer, OfferDetailUpdateSeralizer, OrdersSerializer, OrderDetailSerializer, ReviewListSeralizer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permission import IsBusinessUser, IsOwnerFromOfffer, IsCustomerUser, IsBusinessAndAdminUser, IsCustomerUserForReviews
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListCreateAPIView,ListAPIView
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



class OrderListCreateView(APIView):
    permission_classes = [IsCustomerUser, IsAuthenticated]
    queryset = Orders.objects.all()
    

    def get(self, request):
       
        orders = Orders.objects.filter(customer_user=request.user) | Orders.objects.filter(business_user=request.user)
        serializer = OrdersSerializer(orders, many=True)

        return Response(serializer.data)
    

    def post(self, request):
        
        offer_detail_id = request.data.get('offer_detail_id')
        if not OfferDetails.objects.filter(id=offer_detail_id).exists():
            return Response({"error": "The specified offer details could not be found."}, status=404)
        
        
        serializer = OrdersSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsBusinessAndAdminUser, IsAuthenticated]

class OrderBusinessCountViewInProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id, type='business')
        user = request.user
        if user.id != business_user.id:
            return Response({"order_count": 0})

        count = Orders.objects.filter(business_user=user, status="in_progress").count()
        return Response({"order_count": count})
    
class OrderBusinessCountViewCompleted(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id, type='business')
        user = request.user
        if user.id != business_user.id:
            return Response({"order_count": 0})

        count = Orders.objects.filter(business_user=user, status="completed").count()
        return Response({"order_count": count})


class ReviewFilter(FilterSet):
    business_user_id = NumberFilter(field_name='business_user', lookup_expr='exact')
    reviewer_id = NumberFilter(field_name='reviewer', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id' ]


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSeralizer
    permission_classes = [IsCustomerUserForReviews, IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']


    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        business_user = request.data.get('business_user')
        allowedFields = { 'business_user', 'rating', 'description'  }
        incomingField = set(data.keys())
        invalid_fields = allowedFields - incomingField
        if invalid_fields:
            return Response(
            {"detail": f"Unerlaubte Felder: {invalid_fields}"},
            status=status.HTTP_400_BAD_REQUEST
        )

        seralizer = ReviewListSeralizer(data=request.data)

        if Review.objects.filter(reviewer=user, business_user=business_user ).exists():
            return Response({'You have already reviewed this business.'}, status=status.HTTP_403_FORBIDDEN)


        if seralizer.is_valid():
            seralizer.save(reviewer=user)
            return Response(seralizer.data, status=status.HTTP_201_CREATED)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)            