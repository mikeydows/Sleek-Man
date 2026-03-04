from .models import Cart, CartItem

def cart_items_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []
    return {'cart_items': cart_items}