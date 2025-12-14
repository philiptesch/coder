from django.db import models
from auth_app.models import User

# Create your models here.
class Profile(models.Model):


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