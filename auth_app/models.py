from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User (AbstractUser):

    class UserType(models.TextChoices):
        customer = 'customer', 'customer'
        business = 'business', 'business'

    type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.customer)
    created_at = models.DateTimeField(auto_now_add=True)