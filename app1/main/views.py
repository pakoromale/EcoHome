from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.http import JsonResponse
from .models import Product, Category, Review, Order, OrderItem

# Кастомные формы с русскими подписями
class RussianAuthForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RussianRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': 'Обязательно. Не более 150 символов. Только буквы, цифры и @/./+/-/_.',
        }

# Основные view
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

def cart(request):
    cart_items = []
    total_price = 0
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def checkout(request):
    if request.method == 'POST':
        # Логика оформления заказа
        pass
    return render(request, 'checkout.html')

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        messages.success(request, 'Данные успешно обновлены!')
        return redirect('profile')
    
    return render(request, 'profile.html', {'orders': orders})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = RussianAuthForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = RussianAuthForm()
    
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = RussianRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = RussianRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('home')

@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('home')
    
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    
    return render(request, 'admin.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users
    })

def api_products(request):
    products = Product.objects.filter(is_active=True).values('id', 'name', 'price', 'image')
    return JsonResponse(list(products), safe=False)