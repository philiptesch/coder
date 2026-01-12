from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User (AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Fields:
        - username: Unique username for authentication.
        - type: Type of user ('customer' or 'business').
        - created_at: Timestamp when the user was created.

    UserType:
        - customer: Standard customer user.
        - business: Business user who can create offers.

    Usage:
        - Differentiates between customers and business users.
        - Used for permission checks and linking to offers, orders, and reviews.
    """
    class UserType(models.TextChoices):
        customer = 'customer', 'customer'
        business = 'business', 'business'
    username = models.CharField(max_length=150, unique=True)
    type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.customer)
    created_at = models.DateTimeField(auto_now_add=True)