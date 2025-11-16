from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from .models import Product



# Define the _cart_id function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (total * 2.5) / 100
        grand_total = total + tax

    except Cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


# CART SESSION ID

def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# ADD TO CART

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, cart=cart)

    return redirect('cart')


# DECREASE QUANTITY

def remove_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')


# REMOVE FULL ITEM
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = Product.objects.get(id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except:
        pass

    return redirect('cart')
