from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def product_list(request):
    products = Product.objects.all()
    return render(request, "product.html", {"products": products})
    
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()
    return redirect('product')

def settings(request):
    return render(request, "settings.html")

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        phone = request.POST.get('number')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        # use email as username (clean ecommerce practice)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # save profile phone number
        user.profile.phone_number = phone
        user.profile.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'registration/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'registration/login.html')

def logoutPage(request):
    logout(request)
    return redirect('home')

def termsAndCondition(request):
    return render(request, "terms.html")

def productOverview(request):
    return render(request, "product-overview.html")