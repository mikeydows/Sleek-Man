from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Favorite

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def product_list(request):
    products = Product.objects.all()
    sort = request.GET.get("sort")

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    if sort == "newest":
        products = Product.objects.all().order_by("-id")  # newest first
    elif sort == "low":
        products = Product.objects.all().order_by("price")  # lowest price
    elif sort == "high":
        products = Product.objects.all().order_by("-price")  # highest price
    else:
        products = Product.objects.all()  # default / recommended

    return render(request, "product.html", {
        "products": products,
        "cart_items": cart_items
    })    

@login_required
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(CartItem, id=cart_id, cart__user=request.user)
    cart_item.delete()
    return redirect('product')

@login_required
def add_to_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('product')

@login_required
def favorites_page(request):
    favorite_items = Favorite.objects.filter(user=request.user)
    return render(request, "favorites.html", {
        "favorite": favorite_items
    })

@login_required
def remove_from_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect('favorites')


def cart_page(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    return render(request, "cart.html", {
        "cart_items": cart_items
    })

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
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "registration/login.html")

def logoutPage(request):
    logout(request)
    return redirect('home')

def termsAndCondition(request):
    return render(request, "terms.html")

def productOverview(request):
    return render(request, "product-overview.html")