from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from products.models import Product, Variation


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
        cart = Cart.objects.get(cart_id=_cart_id(request))
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
    # allow variations to be passed either via POST (from product page) or GET (from cart increment link)
    color = request.POST.get('color') or request.GET.get('color_id')
    size = request.POST.get('size') or request.GET.get('size_id')
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        cart.save()

    # resolve Variation objects (if provided)
    color_variation = None
    size_variation = None
    # resolve Variation objects (if provided). If numeric id is provided, resolve by pk.
    color_variation = None
    size_variation = None
    if color:
        # color may be an id (from cart links) or a value (from product detail POST)
        if str(color).isdigit():
            try:
                color_variation = Variation.objects.get(
                    pk=int(color), product=product, variation_category='color')
            except Variation.DoesNotExist:
                color_variation = None
        else:
            try:
                color_variation = Variation.objects.get(
                    product=product, variation_category='color', variation_value__iexact=color)
            except Variation.DoesNotExist:
                color_variation = None

    if size:
        if str(size).isdigit():
            try:
                size_variation = Variation.objects.get(
                    pk=int(size), product=product, variation_category='size')
            except Variation.DoesNotExist:
                size_variation = None
        else:
            try:
                size_variation = Variation.objects.get(
                    product=product, variation_category='size', variation_value__iexact=size)
            except Variation.DoesNotExist:
                size_variation = None

    # try to find an existing cart item for the same product + selected variations
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, variation_color=color_variation, variation_size=size_variation)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, cart=cart,
                                variation_color=color_variation, variation_size=size_variation)

    return redirect('cart')


# DECREASE QUANTITY

def remove_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(cart_id=cart_id(request))

        # variations may be passed via GET query params
        color_id = request.GET.get('color_id')
        size_id = request.GET.get('size_id')

        color_variation = None
        size_variation = None
        if color_id:
            try:
                color_variation = Variation.objects.get(
                    pk=int(color_id), product=product, variation_category='color')
            except Exception:
                color_variation = None
        if size_id:
            try:
                size_variation = Variation.objects.get(
                    pk=int(size_id), product=product, variation_category='size')
            except Exception:
                size_variation = None

        cart_item = CartItem.objects.get(
            product=product, cart=cart, variation_color=color_variation, variation_size=size_variation)

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

    color_id = request.GET.get('color_id')
    size_id = request.GET.get('size_id')

    color_variation = None
    size_variation = None
    if color_id:
        try:
            color_variation = Variation.objects.get(
                pk=int(color_id), product=product, variation_category='color')
        except Exception:
            color_variation = None
    if size_id:
        try:
            size_variation = Variation.objects.get(
                pk=int(size_id), product=product, variation_category='size')
        except Exception:
            size_variation = None

    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, variation_color=color_variation, variation_size=size_variation)
        cart_item.delete()
    except:
        pass

    return redirect('cart')
