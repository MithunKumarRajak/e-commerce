from django.urls import path
from .views import products
urlpatterns = [
    path('', products, name='products'),
    path('<slug:category_slug>', products, name='products_by_category'),
]
