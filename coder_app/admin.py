from django.contrib import admin
from .models import offers, OfferDetails, Orders, Review
# Register your models here.
admin.site.register([offers, OfferDetails, Orders, Review])