from django.shortcuts import redirect, render, get_object_or_404
from category.models import Category
from .models import Product, ProductGallery
from carts.models import CartItem, Cart
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from products.forms import ReviewForm
from products.models import ReviewRating
from orders.models import OrderProduct


def products(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)
    product_gallery = ProductGallery.objects.filter(product=product)

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product=product).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
            
    else:
        orderproduct = None
        
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
    except Cart.DoesNotExist:
        in_cart = False
        
    # get the reviews
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    

    context = {
        'product': product,
        'category': category,
        'product_gallery': product_gallery,
        'in_cart': in_cart,
        'reviews': reviews,
        'orderproduct': orderproduct,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    keyword = request.GET.get('keyword') or request.GET.get('search')

    if keyword:
        products = Product.objects.filter(
            Q(description__icontains=keyword) |
            Q(product_name__icontains=keyword),
            is_available=True
        ).order_by('-created_date')
    else:
        products = Product.objects.none()  # no keyword → no results

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)


# Submit Review View
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(
                request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, 'Thank you! Your review has been submitted.')
                return redirect(url)


