from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def product(request):
    return render(request, "product.html")

def settings(request):
    return render(request, "settings.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("number")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        Profile.objects.create(
            user=user,
            phone_number=phone
        )

        messages.success(request, "Account created successfully")
        return redirect("home")

    return render(request, "registration/signup.html")

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
