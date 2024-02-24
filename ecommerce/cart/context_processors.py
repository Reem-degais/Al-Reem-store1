from .models import Cart, CartItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist

#count cart items and show it on cart icon on navbar

def count(request):
    cart_counter = 0
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user)
        else:
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
        for cart_item in cart_items:
            cart_counter += cart_item.quantity 
    except Cart.DoesNotExist:
        cart_counter = 0

    return dict(cart_counter=cart_counter)