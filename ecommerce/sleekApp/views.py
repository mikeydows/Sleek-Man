from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")

        if password1 != password2:
            messages.error(request, "password doesnt match... Try again!")
            return redirect("signup")
        
        if username is None:
            messages.error(request, "Username cannot be empty")
            return redirect("signup")
        
        if email is None:
            messages.error(request, "emake sure to enter the correct email")
            return redirect("signup")

        if User.objects.filter(username = username).exists():
            messages.error(request, "Usrname exist, Try logging in")
            return redirect("signup")


        user = User.objects.create_user(
                username = username,
                email = email,
                password = password1,
                )
        
        login(user)
        return redirect("home")
    return render (request, "registration/signup.html")

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request, 
            username = username, 
            password = password
        )

        if user is None:
            messages.error(request, "Wrong credentials, Try again")
            return redirect("login")
        else:
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html")

def logoutPage(request):
    logout(request)
    return redirect('home')
