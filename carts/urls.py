from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
     path('increment/<int:cart_item_id>/', views.increment_cart, name='increment_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    
]
