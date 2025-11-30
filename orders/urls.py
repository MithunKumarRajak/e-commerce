from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('cod_payments/', views.cod_payments, name='cod_payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('download_invoice/', views.download_invoice, name='download_invoice'),
    path('track/<str:order_number>/', views.order_tracking, name='order_tracking'),


]
