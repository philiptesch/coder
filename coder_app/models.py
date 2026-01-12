from django.db import models
from auth_app.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Offers(models.Model):
    """
    Represents an offer created by a business user.

    Fields:
        - user: The business user who owns the offer.
        - title: Title of the offer.
        - image: Optional image associated with the offer.
        - description: Detailed description of the offer.
        - created_at: Timestamp when the offer was created.
        - updated_at: Timestamp when the offer was last updated.

    Usage:
        - Main model for storing offers.
        - Linked to OfferDetails for pricing, delivery, and features.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='Offers/', default=True, null=True,)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    


    

class OfferDetails(models.Model):
    """
    Represents detailed options for an offer.

    Fields:
        - offer: ForeignKey to the parent offer.
        - revisions: Number of revisions included in this detail.
        - title: Title of the detail option.
        - delivery_time: Delivery time in days.
        - price: Price of this offer detail.
        - features: JSON list of included features.
        - offer_type: Type of the offer (basic, standard, premium).

    Usage:
        - Each offer can have multiple details.
        - Used for filtering, pricing, and delivery time aggregation.
    """

    class OfferTyp(models.TextChoices):
        basic = 'basic', 'basic'
        standard = 'standard', 'standard'
        premium = 'premium', 'premium'


    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name='details')
    revisions = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    delivery_time = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=20, choices=OfferTyp.choices, default=OfferTyp.basic)
    def __str__(self):
        return self.title
    
class Orders(models.Model):
    """
    Represents an order placed by a customer for a specific offer detail.

    Fields:
        - customer_user: The customer who placed the order.
        - business_user: The business that owns the offer.
        - offer_detail: The specific offer detail selected by the customer.
        - created_at: Timestamp when the order was created.
        - updated_at: Timestamp when the order was last updated.
        - status: Current status of the order (in_progress, completed, canceled).

    Usage:
        - Tracks the lifecycle of customer orders.
        - Used for order management and business statistics.
    """

    class Status(models.TextChoices):
        in_progress = 'in_progress', 'in_progress'
        completed = 'completed', 'completed'
        canceled = 'canceled', 'canceled'

    customer_user = models.ForeignKey(User, related_name='customer_orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(User, related_name='business_orders', on_delete=models.CASCADE)
    offer_detail = models.ForeignKey(OfferDetails, related_name='details', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.in_progress)

    def __str__(self):
        return f"Order {self.id} by {self.customer_user.username}"
    

class Review(models.Model):
    """
    Represents a customer review for a business user.

    Fields:
        - business_user: The business user being reviewed.
        - reviewer: The customer who wrote the review.
        - rate: Rating given to the business (0.0 - 10.0).
        - description: Optional text description of the review.
        - created_at: Timestamp when the review was created.
        - updated_at: Timestamp when the review was last updated.

    Usage:
        - Tracks customer feedback for businesses.
        - Used for calculating average ratings and review statistics.
    """
    business_user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='given_reviews', on_delete=models.CASCADE)
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.business_user.username} - Rating: {self.rate}"