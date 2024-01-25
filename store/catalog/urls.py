from django.urls import path
from .views import CatalogView


app_name = 'catalog'

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
]