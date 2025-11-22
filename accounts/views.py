from django.shortcuts import redirect, render
from django.contrib import messages
try:
    import requests
except Exception:
    requests = None
from carts.models import Cart, CartItem
from .forms import RegistrationForm
from .models import Account
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
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            # User Activation can be added here
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

            # messages.success(request, 'You are registered successfully! and a verification email has been sent to your email address. Please verify to activate your account.')
            return redirect('/accounts/login/?command=login&email='+email)

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
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items_exists = CartItem.objects.filter(cart=cart).exists()
                if cart_items_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_items:
                        variation = item.variation_color
                        product_variation.append(list(variation.variation))

                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    # product variation
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(
                                product=item.product, id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(
                                cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
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
            # Provide clearer feedback: distinguish between inactive accounts
            # (user registered but not activated) and genuinely wrong credentials.
            try:
                existing = Account.objects.get(email=email)
                if not existing.is_active:
                    messages.error(
                        request, 'Account is not activated. Please check your email for the activation link.')
                else:
                    messages.error(request, 'Invalid login credentials')
            except Account.DoesNotExist:
                messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

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


@login_required(login_url='login')
def dashboard(request):
    # Provide safe context expected by the template
    orders_count = 0
    # userprofile may not exist in this project; provide fallback

    class _Profile:
        class _Pic:
            url = '/static/images/default_profile.png'

        profile_picture = _Pic()

    userprofile = getattr(request.user, 'userprofile', _Profile())

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)
