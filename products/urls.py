from django.urls import path
from .views import *


urlpatterns = [
    path('', products, name='products'),
    path('category/<slug:category_slug>/',
         products, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',
         product_detail, name='product_detail'),
    path('search/', search, name='search'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),
    path('submit_review/<int:product_id>/',submit_review, name='submit_review'),

]
