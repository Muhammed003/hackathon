from django.contrib import admin
from .models import ShoppingCart, CartItem
# Register your models here.
admin.site.register(ShoppingCart)
admin.site.register(CartItem)