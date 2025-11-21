from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('download_invoice/', views.download_invoice, name='download_invoice'),


]
