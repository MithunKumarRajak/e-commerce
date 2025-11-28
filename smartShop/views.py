
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
