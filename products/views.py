from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import *
from carts.models import CartItem
from carts.views import _cart_id
from carts.models import Cart
# Create your views here


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


# Single product details
def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)
    product_gallery = ProductGallery.objects.filter(product=product)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
    except Cart.DoesNotExist:
        in_cart = False

    context = {
        'product': product,
        'category': category,
        'product_gallery': product_gallery,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)
