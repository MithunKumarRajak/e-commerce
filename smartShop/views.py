
from django.shortcuts import render, redirect
from products.models import Product
# Create your views here.
from category.models import Category
from .models import Contact
from django.contrib import messages



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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone = request.POST.get('phone', '')
        
        # Save to database
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            phone=phone
        )
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
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

def returns(request):
    return render(request, 'pages/returns.html')

def support(request):
    return render(request, 'pages/support.html')

