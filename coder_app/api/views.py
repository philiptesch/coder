from profile_app.models import Profile
from auth_app.models import User
from coder_app.models import Offers, OfferDetails, Orders, Review

from rest_framework.views import APIView
from .seralizers import (
    OfferSeralizer,
    OfferCreateSeralizer,
    OfferDetailSeralizer,
    OfferDetailRetrieveSeralizer,
    OfferDetailUpdateSeralizer,
    OrdersSerializer,
    OrderDetailSerializer,
    ReviewListSeralizer,
    ReviewDetailSeralizer,
    BaseSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permission import (
    IsBusinessUser,
    IsOwnerFromOfffer,
    IsCustomerUser,
    IsBusinessAndAdminUser,
    IsCustomerUserForReviews,
    isReviewer
)
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    ListAPIView
)
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import FilterSet, NumberFilter, DjangoFilterBackend
from django.db.models import Min, Max
from rest_framework.exceptions import PermissionDenied, ValidationError


class OfferListPagination(PageNumberPagination):
    # Default number of items per page
    page_size = 5

    # Allow client to override page size
    page_size_query_param = 'page_size'

    # Maximum allowed page size
    max_page_size = 100


class OfferFilterSet(FilterSet):
    creator_id = NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = Offers
        fields = ['creator_id']



class OfferListView(ListCreateAPIView):
    """
    List all offers or create a new offer.

    Permissions:
        Only business users are allowed to access this endpoint.

    Behavior:
        - GET: Returns a paginated list of all offers.
        - POST: Creates a new offer for the authenticated business user.

    Filtering:
        - creator_id: Filter offers by creator (business user ID).
        - min_price: Filter offers by minimum price (based on offer details).
        - max_delivery_time: Filter offers by maximum delivery time.

    Search:
        - title
        - description

    Ordering:
        - updated_at
        - min_price

    Pagination:
        Uses OfferListPagination.
    """
    permission_classes = [IsBusinessUser]
    pagination_class = OfferListPagination
    queryset = Offers.objects.all()

    # Enable filtering, searching and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = OfferFilterSet
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSeralizer
        return OfferSeralizer

    def get_queryset(self):
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        min_price = self.request.query_params.get('min_price')

        queryset = Offers.objects.all()


        if max_delivery_time is not None:
            try:
                max_delivery_time = int(max_delivery_time)
            except ValueError:
                raise ValidationError("max_delivery_time must be an integer.")

            queryset = queryset.filter(
                details__delivery_time__lte=max_delivery_time
            )

        if min_price is not None:
            try:
                min_price = float(min_price.replace(',', '.'))
            except ValueError:
                raise ValidationError({"min_price": "Must be a number."})

            queryset = queryset.annotate(
                min_price=Min('details__price')
            ).filter(min_price__gte=min_price)

        return queryset.distinct()



class OfferDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single offer.

    Permissions:
        - User must be authenticated.
        - Only the owner of the offer is allowed to update or delete it.

    Behavior:
        - GET: Retrieve offer details.
        - PUT/PATCH: Update offer data.
        - DELETE: Remove the offer.
    """
    queryset = Offers.objects.all()
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
    """
    Retrieve a single offer detail.

    Permissions:
        User must be authenticated.

    Behavior:
        - GET: Returns detailed information about one offer detail.
    """
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailRetrieveSeralizer
    permission_classes = [IsAuthenticated]


class OrderListCreateView(APIView):
    """
    List user-related orders or create a new order.

    Permissions:
        - User must be authenticated.
        - Only customers are allowed to create orders.

    Behavior:
        - GET: Returns all orders where the user is customer or business.
        - POST: Creates a new order for an offer detail.

    Restrictions:
        - Users cannot order their own offers.
    """
    permission_classes = [IsCustomerUser, IsAuthenticated]
    queryset = Orders.objects.all()

    def get(self, request):
        orders = ( Orders.objects.filter(customer_user=request.user) |Orders.objects.filter(business_user=request.user))
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        offer_detail_id = request.data.get('offer_detail_id')
        try:
            offer_detail_id = int(offer_detail_id)
        except (ValueError, TypeError):
            return Response({"error": "offer_detail_id must be an integer or a string with a valid number."},status=status.HTTP_400_BAD_REQUEST)

        if not OfferDetails.objects.filter(id=offer_detail_id).exists():
            return Response({"error": "The specified offer details could not be found."},status=404)
        offer_detail = OfferDetails.objects.get(id=offer_detail_id)

        if offer_detail.offer.user == request.user:return Response({"error": "You cannot order your own offer."},status=status.HTTP_403_FORBIDDEN)

        serializer = OrdersSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an order.

    Permissions:
        - User must be authenticated.
        - Only business users or admins are allowed.

    Behavior:
        - PUT/PATCH: Update order data.
        - DELETE: Delete the order.
    """
    queryset = Orders.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsBusinessAndAdminUser, IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Orders, pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj


class OrderBusinessCountViewInProgress(APIView):
    """
    Return the number of in-progress orders for a business user.

    Permissions:
        User must be authenticated.

    Behavior:
        - GET: Returns the count of orders with status 'in_progress'.

    Notes:
        Only the business owner can see their order count.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id, type='business')
        user = request.user
        if user.id != business_user.id:
            return Response({"order_count": 0})

        count = Orders.objects.filter(business_user=user,status="in_progress").count()
        return Response({"order_count": count})


class OrderBusinessCountViewCompleted(APIView):
    """
    Return the number of completed orders for a business user.

    Permissions:
        User must be authenticated.

    Behavior:
        - GET: Returns the count of orders with status 'completed'.

    Notes:
        Only the business owner can see their completed order count.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User,id=business_user_id,type='business')
        user = request.user

        if user.id != business_user.id:
            return Response({"completed_order_count": 0})

        count = Orders.objects.filter(business_user=user,status="completed").count()
        return Response({"completed_order_count": count})



class ReviewFilter(FilterSet):
    """
    Filter configuration for reviews.

    Filtering:
        - business_user_id: Filter reviews by business user ID.
        - reviewer_id: Filter reviews by reviewer (customer) ID.
    """
    business_user_id = NumberFilter(field_name='business_user',lookup_expr='exact')
    reviewer_id = NumberFilter(field_name='reviewer',lookup_expr='exact')
    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']


class ReviewListView(generics.ListCreateAPIView):
    """
    List all reviews or create a new review.

    Permissions:
        - User must be authenticated.
        - Only customer users are allowed to create reviews.

    Filtering:
        - Filter by business_user_id.
        - Filter by reviewer_id.

    Ordering:
        - updated_at
        - rating

    Behavior:
        - GET: Returns a list of reviews.
        - POST: Creates a new review if the user is eligible.

    Restrictions:
        - A customer can review a business only once.
    """
    
    queryset = Review.objects.all()
    serializer_class = ReviewListSeralizer
    permission_classes = [IsCustomerUserForReviews,IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def create(self, request, *args, **kwargs):
        user = request.user
        business_user = request.data.get('business_user')

        if user.type != 'customer':
            return Response({'only customer are allowed to do reviews.'},status=status.HTTP_403_FORBIDDEN)

        if Review.objects.filter(reviewer=user,business_user=business_user).exists():
            return Response({'You have already reviewed this business.'},status=status.HTTP_400_BAD_REQUEST)

        seralizer = ReviewListSeralizer(data=request.data)

        if seralizer.is_valid():
            seralizer.save(reviewer=user)
            return Response(seralizer.data,status=status.HTTP_201_CREATED)

        return Response(seralizer.errors,status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    """
    Update or delete a single review.

    Permissions:
        - User must be authenticated.
        - Only the original reviewer is allowed.

    Behavior:
        - PATCH: Partially update the review.
        - DELETE: Remove the review.

    Update restrictions:
        Only the following fields can be updated:
            - rating
            - description
    """
    permission_classes = [isReviewer, IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        review = get_object_or_404(Review, pk=pk)
        allowedFields = {'rating', 'description'}
        incomingFields = set(request.data.keys())
        invalid_fields = incomingFields - allowedFields
        if invalid_fields:
            return Response({"detail": f"Unauthorized fields: {invalid_fields}"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.user != review.reviewer:
            return Response({'detail': 'The user is not authorized to edit this review.'},status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewDetailSeralizer(review,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        review = get_object_or_404(Review, pk=pk)

        if request.user != review.reviewer:
            return Response({'detail': 'Cannot delete this review.'},status=403)

        review.delete()

        return Response({'detail': 'review deleted successfully.'},status=204)


class BaseInfoView(APIView):
    """
    Return base application information.

    Permissions:
        Public access (no authentication required).

    Behavior:
        - GET: Returns base data for the application.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = BaseSerializer(data={})
        serializer.is_valid()
        return Response(serializer.data)
