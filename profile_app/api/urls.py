from django.urls import path
from .views import ProfileDetailView, BusinessDetailView, CustomerDetailView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessDetailView.as_view(), name='business-profile-list'),
    path('profiles/customer/', CustomerDetailView.as_view(), name='customer-profile-list'),
]