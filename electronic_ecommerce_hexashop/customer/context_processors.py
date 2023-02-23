from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser



# @login_required
# def counter(request):
#     count = 0
#     try:
#         cart =Cart.objects.get_or_create(user = request.user)
#         cart_items = CartItems.objects.all().filter(cart=cart)
#         for cart_item in cart_items:
#             count += cart_item.quantity
#     except Cart.DoesNotExist:
#         count = 0
#     context = {"count": count}
#     return context



def cart_count(request):
    counter = 0
    if isinstance(request.user, AnonymousUser):
        return {}
    try:
        cart = Cart.objects.get(user=request.user, oredered=False)
    except Cart.DoesNotExist:
        return {}
    cart_items = CartItems.objects.filter(cart=cart)
    for cart_item in cart_items:
        counter += cart_item.quantity
    context = {"counter": counter}
    return context



def wishlist_count(request):
    if isinstance(request.user, AnonymousUser):
        return {}
    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        return {}
    count = wishlist.product.count()
    return {'wishlist_count': count}

