from django.urls import path
from . import views
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView

class GoogleLoginDirect(OAuth2LoginView):
    adapter_class = GoogleOAuth2Adapter


urlpatterns = [
    path("", views.home, name = "home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("product/", views.product_list, name="product"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("about/", views.about, name="about" ),
    path("settings/", views.settings, name="settings"),
]