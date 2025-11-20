from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),


]
