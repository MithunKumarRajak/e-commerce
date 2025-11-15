from django.urls import path
from .views import *


urlpatterns = [
    path('', products, name='products'),
    path('<slug:category_slug>/',
         products, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',
         product_detail, name='product_detail'),
]
