from django.urls import path
from .views import calculate_price

urlpatterns = [
    path('calculate-price/', calculate_price, name='calculate_price'),
]
