from django.urls import path
from .views import ProductDetails


app_name = 'details'

urlpatterns = [
    path('<slug:slug>/', ProductDetails.as_view(), name='product_details')
]

