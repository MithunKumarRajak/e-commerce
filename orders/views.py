from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from orders.forms import OrderForm
from .models import Order, Payment, OrderProduct
from products.models import Product
from django.core.mail import EmailMessage
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
import datetime
import json
from django.contrib.auth.decorators import login_required
import razorpay
from decouple import config
import hmac
import hashlib


@login_required
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


@login_required
def cod_payments(request):
    if request.method != 'POST':
        return redirect('products')

    order_id = request.POST.get('orderID')
    try:
        order = Order.objects.get(
            user=request.user, is_ordered=False, order_number=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('checkout')

    # Create COD payment record
    payment_id = f"COD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{order.id}"
    payment = Payment(
        user=request.user,
        payment_id=payment_id,
        payment_method='Cash On Delivery',
        amount_paid=order.order_total,
        status='Pending',
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move cart items to OrderProduct table and adjust stock
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        product_variation = item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send confirmation email
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Redirect to order complete
    redirect_url = reverse(
        'order_complete') + f'?order_number={order.order_number}&payment_id={payment.payment_id}'
    return redirect(redirect_url)


def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('products')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number using timestamp + id for uniqueness
            order_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(data.id)
            data.order_number = order_number
            data.save()
            # If the user chose Cash on Delivery, finalize the order now
            payment_method = request.POST.get('payment_method', '').upper()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            if payment_method == 'COD' or payment_method == 'CASH_ON_DELIVERY' or payment_method == 'CASH ON DELIVERY':
                # Create a Payment record to record COD choice
                payment_id = f"COD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{order.id}"
                payment = Payment(
                    user=current_user,
                    payment_id=payment_id,
                    payment_method='Cash On Delivery',
                    amount_paid=order.order_total,
                    status='Pending',
                )
                payment.save()

                order.payment = payment
                order.is_ordered = True
                order.save()

                # Move the cart items to OrderProduct table
                cart_items = CartItem.objects.filter(user=current_user)

                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()

                    product_variation = item.variations.all()
                    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                    orderproduct.variations.set(product_variation)
                    orderproduct.save()

                    # Reduce stock
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()

                # Clear cart
                CartItem.objects.filter(user=current_user).delete()

                # Send order received email
                mail_subject = 'Thank you for your order!'
                message = render_to_string('orders/order_recieved_email.html', {
                    'user': request.user,
                    'order': order,
                })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                # Redirect to order complete page with order_number and payment id
                redirect_url = reverse(
                    'order_complete') + f'?order_number={order.order_number}&payment_id={payment.payment_id}'
                return redirect(redirect_url)

            # Otherwise render payment page for online payment providers (e.g., PayPal)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return redirect('checkout')
    return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


@login_required
def download_invoice(request):
    """Return an HTML invoice as an attachment for the logged-in user's order.

    This is a simple 'download as HTML' implementation suitable for local
    use. For PDF generation consider xhtml2pdf/weasyprint later.
    """
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')
    try:
        order = Order.objects.get(
            order_number=order_number, is_ordered=True, user=request.user)
        payment = Payment.objects.get(payment_id=payment_id)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }

        html = render(request, 'orders/order_complete.html', context).content
        filename = f"invoice-{order.order_number}.html"
        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except (Order.DoesNotExist, Payment.DoesNotExist):
        messages.error(request, 'Invoice not found.')
        return redirect('order_list')


@login_required
def order_list(request):
    """List the current user's completed orders."""
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    # Reuse the account-facing orders template to avoid duplicates
    return render(request, 'accounts/my_orders.html', context)


@login_required
def order_tracking(request, order_number):
    """Display order tracking page with status timeline."""
    try:
        order = Order.objects.get(
            order_number=order_number,
            user=request.user,
            is_ordered=True
        )
        order_products = OrderProduct.objects.filter(order_id=order.id)

        context = {
            'order': order,
            'order_products': order_products,
        }
        return render(request, 'orders/order_tracking.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('my_orders')


@login_required
def razorpay_create_order(request):
    """Create a Razorpay order for payment processing."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    try:
        body = json.loads(request.body)
        order_id = body.get('orderID')
        amount = float(body.get('amount'))
        
        # Get the order from database
        order = Order.objects.get(
            user=request.user, 
            is_ordered=False, 
            order_number=order_id
        )
        
        # Initialize Razorpay client
        razorpay_key_id = config('RAZORPAY_KEY_ID')
        razorpay_key_secret = config('RAZORPAY_KEY_SECRET')
        client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
        
        # Create Razorpay order
        # Amount should be in paise (multiply by 100)
        razorpay_order = client.order.create({
            'amount': int(amount * 100),
            'currency': 'INR',
            'payment_capture': 1
        })
        
        return JsonResponse({
            'razorpay_order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency']
        })
        
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def razorpay_callback(request):
    """Handle Razorpay payment callback and verify signature."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    try:
        body = json.loads(request.body)
        order_id = body.get('orderID')
        razorpay_payment_id = body.get('razorpay_payment_id')
        razorpay_order_id = body.get('razorpay_order_id')
        razorpay_signature = body.get('razorpay_signature')
        
        # Get the order
        order = Order.objects.get(
            user=request.user,
            is_ordered=False,
            order_number=order_id
        )
        
        # Verify payment signature
        razorpay_key_secret = config('RAZORPAY_KEY_SECRET')
        
        # Generate signature to verify
        generated_signature = hmac.new(
            razorpay_key_secret.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature != razorpay_signature:
            return JsonResponse({
                'success': False,
                'error': 'Payment signature verification failed'
            }, status=400)
        
        # Payment verified successfully, create Payment record
        payment = Payment(
            user=request.user,
            payment_id=razorpay_payment_id,
            payment_method='Razorpay',
            amount_paid=order.order_total,
            status='COMPLETED',
        )
        payment.save()
        
        # Update order
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        # Move cart items to OrderProduct table
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()
            
            # Set variations
            product_variation = item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
            
            # Reduce stock
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()
        
        # Clear cart
        CartItem.objects.filter(user=request.user).delete()
        
        # Send confirmation email
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'payment_id': payment.payment_id
        })
        
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Order not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
