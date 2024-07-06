from django.urls import path
from .views import calculate_price

urlpatterns = [
    path('calculate_price/', calculate_price, name='calculate_price'),
]
