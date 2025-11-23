from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    # Email Verification
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPasswordValidate/<uidb64>/<token>/',
         views.resetPasswordValidate, name='resetPasswordValidate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),

    # Orders
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<str:order_id>/',
         views.order_detail, name='order_detail'),






]
