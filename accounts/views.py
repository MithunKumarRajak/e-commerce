from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from orders.models import Order, OrderProduct
from carts.models import Cart, CartItem
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.views import _cart_id
import requests


# Create your views here.

# Registration View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            
            # Check if email already exists
            if Account.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists. Please use a different email or login.')
                return redirect('register')
            
            # Check if username already exists (in case of collision)
            base_username = username
            counter = 1
            while Account.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            try:
                # Create user
                user = Account.objects.create_user(
                    first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.phone_number = phone_number
                # Activate user immediately (no email verification)
                user.is_active = True
                user.save()

                # UserProfile is automatically created by the post_save signal
                # Set default profile picture
                user.userprofile.profile_picture = 'default/user-default.png'
                user.userprofile.save()

                # Transfer guest cart items to new user
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart_items = CartItem.objects.filter(cart=cart)
                    
                    for cart_item in cart_items:
                        # Transfer cart item to the new user
                        cart_item.user = user
                        cart_item.cart = None
                        cart_item.save()
                except Cart.DoesNotExist:
                    pass
                except Exception as e:
                    # Log error but don't prevent registration
                    print(f"Error transferring cart during registration: {e}")

                # Auto-login the user after registration
                auth.login(request, user)
                messages.success(request, f'Welcome {first_name}! Your account has been created successfully.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Registration failed. Please try again. Error: {str(e)}')
                return redirect('register')

    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

# Login View


def login(request):
    if request.method == 'POST':
        # Handle login logic here
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Use username kwarg because Django's authentication backend expects
        # the USERNAME_FIELD value under the `username` parameter. Our
        # custom user model sets `USERNAME_FIELD = 'email'`, so passing the
        # email as `username` ensures ModelBackend will authenticate correctly.
        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            # Transfer guest cart items to user cart
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    
                    # Get list of cart items with their variations
                    for cart_item in cart_items:
                        product_variations = list(cart_item.variations.all())
                        
                        # Check if user already has this product with same variations
                        try:
                            user_cart_item = CartItem.objects.get(
                                user=user,
                                product=cart_item.product,
                            )
                            
                            # Check if variations match
                            existing_variations = list(user_cart_item.variations.all())
                            
                            if set(product_variations) == set(existing_variations):
                                # Same product with same variations - increase quantity
                                user_cart_item.quantity += cart_item.quantity
                                user_cart_item.save()
                            else:
                                # Same product but different variations - create new cart item
                                cart_item.user = user
                                cart_item.cart = None
                                cart_item.save()
                        
                        except CartItem.DoesNotExist:
                            # Product doesn't exist in user cart - transfer it
                            cart_item.user = user
                            cart_item.cart = None
                            cart_item.save()
                        
                        except CartItem.MultipleObjectsReturned:
                            # Multiple items exist - find matching one or create new
                            user_cart_items = CartItem.objects.filter(
                                user=user,
                                product=cart_item.product
                            )
                            
                            matched = False
                            for user_item in user_cart_items:
                                existing_variations = list(user_item.variations.all())
                                if set(product_variations) == set(existing_variations):
                                    user_item.quantity += cart_item.quantity
                                    user_item.save()
                                    matched = True
                                    break
                            
                            if not matched:
                                cart_item.user = user
                                cart_item.cart = None
                                cart_item.save()
                    
            except Cart.DoesNotExist:
                pass
            except Exception as e:
                # Log the error but don't prevent login
                print(f"Error transferring cart: {e}")
                pass
            
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            url = request.META.get('HTTP_REFERER')
            if requests:
                try:
                    query = requests.utils.urlparse(url).query
                    # next=/cart/checkout/
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except Exception:
                    pass
            return redirect('dashboard')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


# Account Activation


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

    return render(request, 'accounts/activate.html')


# Forgot Password
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')

# Reset Password Validate


def resetPasswordValidate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            try:
                user = Account.objects.get(pk=uid)
            except Account.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect('resetPassword')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


def resend_activation(request):
    """Allow a user to request a new activation email if their token expired."""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(
                request, 'No account found with that email address.')
            return render(request, 'accounts/resend_activation.html')

        if user.is_active:
            messages.info(
                request, 'Account is already active. You can log in.')
            return redirect('login')

        # Build activation email
        current_site = get_current_site(request)
        mail_subject = 'Please activate your account'
        message = render_to_string('accounts/account_verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        # Redirect to login with an informational query param
        return redirect(f"/accounts/login/?command=verification&email={email}")

    return render(request, 'accounts/resend_activation.html')

# Dashboard


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(
        user_id=request.user.id, is_ordered=True)
    # Provide safe context expected by the template
    orders_count = orders.count()
# user profile picture
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,

    }
    return render(request, 'accounts/dashboard.html', context)


#
@login_required(login_url='login')
def my_orders(request):
    """List completed orders for the logged-in user."""
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)


# edit_profile
@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)


# change password
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(
                request, 'New password and confirm password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


# order detail
@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    context = {
        'order_detail': order_detail,
        'order': order,
    }
    return render(request, 'accounts/order_detail.html', context)
