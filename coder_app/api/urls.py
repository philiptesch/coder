from django.urls import path
from .views import OfferListView, OfferDetailView, OfferDetailRetrieveView

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-details'),
    path('offers/offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(), name='offer-retrieve-details'),
]