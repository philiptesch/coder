from django.urls import path
from .views import OfferListView, OfferDetailView, OfferDetailRetrieveView, OrderListCreateView, OrderDetailView, OrderBusinessCountViewInProgress, OrderBusinessCountViewCompleted, ReviewListView


urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-details'),
    path('offers/offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offer-retrieve-details'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', OrderBusinessCountViewInProgress.as_view(), name='orderbusinesscountInProgress-view'),
    path('completed-order-count/<int:business_user_id>/', OrderBusinessCountViewCompleted.as_view(), name='orderbusinesscountCompleted-view'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),

]