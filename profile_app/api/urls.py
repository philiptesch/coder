from django.urls import path
from .views import ProfileDetailView, BusinessDetailView, CustomerDetailView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/business/', BusinessDetailView.as_view(), name='business-profile-list'),
    path('profile/customer/', CustomerDetailView.as_view(), name='customer-profile-list'),
]