from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import Product

# Create your views here.

# Create your views here.


def products(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        products = Product.objects.filter(
            category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.filter(
            is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)

    context = {
        'product': product,
        'category': category,
    }
    return render(request, 'store/product_detail.html', context)




