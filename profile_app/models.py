from django.db import models
from auth_app.models import User


class Profile(models.Model):
    """
    Represents a user profile containing additional information 
    about a User in the system.

    Fields:
        user: One-to-one relationship to the User model.
        first_name: Optional first name of the user.
        last_name: Optional last name of the user.
        location: Optional location of the user.
        tel: Optional telephone number.
        description: Optional textual description or bio.
        working_hours: Optional working hours info (for business users).
        file: Optional profile picture or document upload.
        created_at: Timestamp for when the profile was created.

    Methods:
        __str__(): Returns a human-readable string representation of the profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=100,blank=True)
    last_name = models.TextField(max_length=100,blank=True)
    location = models.TextField(max_length=100,blank=True)
    tel = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s profile"