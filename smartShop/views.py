
from django.shortcuts import render
from products.models import Product
# Create your views here.
from category.models import Category



def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(
        is_available=True).order_by('-created_date')[:8]

    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def policy(request):
    return render(request, 'policy.html')


def terms(request):
    return render(request, 'terms.html')

# New Views for Footer Links
def careers(request):
    return render(request, 'pages/careers.html')

def press(request):
    return render(request, 'pages/press.html')

def payments(request):
    return render(request, 'pages/payments.html')

def shipping(request):
    return render(request, 'pages/shipping.html')

def cancellation(request):
    return render(request, 'pages/cancellation.html')

def faq(request):
    return render(request, 'pages/faq.html')

def security(request):
    return render(request, 'pages/security.html')

def privacy(request):
    return render(request, 'pages/privacy.html')

