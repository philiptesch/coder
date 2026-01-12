from django.contrib import admin
from .models import Offers, OfferDetails, Orders, Review
# Register your models here.
admin.site.register([Offers, OfferDetails, Orders, Review])