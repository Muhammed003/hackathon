from django.conf import settings
from django.db import models
from django.db import models
from django.contrib.auth.models import User

from apps.product.models import Product


class ShoppingCart(models.Model):
    """
    Корзинa user
    """
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_total_all_price(self):
        cart_items = self.cart_item.all()
        total = sum([item.get_total_price_item() for item in cart_items])
        return total

    def __str__(self):
        return f'cart_id:{self.id} owner:{self.user}'


class CartItem(models.Model):
    """
    Предмет в корзине
    """
    product: Product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True, related_name='product_in_cart')
    cart_shopping = models.ForeignKey(to=ShoppingCart, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price_item(self):
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f'{self.id}) {self.cart_shopping.user.email}'
