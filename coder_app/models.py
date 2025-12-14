from django.db import models
from auth_app.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models her


class offers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='offers/', default=True)
    description = models.TextField()
    createad_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    

class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class OfferDetails(models.Model):


    class OfferTyp(models.TextChoices):
        basic = 'basic', 'basic'
        standard = 'standard', 'standard'
        premium = 'premium', 'premium'


    offer = models.ForeignKey(offers, on_delete=models.CASCADE)
    revision = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    delivery_time = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField('Feature', blank=True)
    offer_type = models.CharField(max_length=20, choices=OfferTyp.choices, default=OfferTyp.basic)
    def __str__(self):
        return self.title
    
class Orders(models.Model):

    class Status(models.TextChoices):
        in_progress = 'in_progress', 'in_progress'
        completed = 'completed', 'completed'
        canceled = 'canceled', 'canceled'

    customer_user = models.ForeignKey(User, related_name='customer_orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(User, related_name='business_orders', on_delete=models.CASCADE)
    offer_detail = models.ForeignKey(OfferDetails, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.in_progress)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

class Review(models.Model):
    business_user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='given_reviews', on_delete=models.CASCADE)
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for Order {self.order.id} - Rating: {self.rating}"