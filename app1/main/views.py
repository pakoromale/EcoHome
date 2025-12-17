from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Category, Review
from .forms import RegistrationForm

def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    return render(request, 'home.html', {'products': products})

def catalog(request):
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)
    
    categories = Category.objects.all()
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product, is_approved=True)
    return render(request, 'product.html', {
        'product': product,
        'reviews': reviews
    })

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

# Остальные view позже добавим
def cart(request):
    return render(request, 'cart.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')