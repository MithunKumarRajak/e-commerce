"""
URL configuration for smartShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from email import policy
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', include('products.urls')),
    path('cart/', include('carts.urls')),
    # Provide a root-level alias for checkout to match previous projects
    path('checkout/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    # Orders
    path('orders/', include('orders.urls')),
    # Add the about, contact, policy, and terms pages
    path('about/' , about, name='about'),
    path('contact/' , contact, name='contact'),
    path('policy/' , policy, name='policy'),    
    path('terms/' , terms, name='terms'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
