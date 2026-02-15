from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("product/", views.product, name="product"),
    path("about/", views.about, name="about" ),
    path("settings/", views.settings, name="settings"),

]