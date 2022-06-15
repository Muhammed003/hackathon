from django.db import models
from apps.cart.models import ShoppingCart
from apps.product.models import Product


class Order(models.Model):
    PAY_CHOICES = (
        ("cash", "cash"),
        ("card", "Credit card"),
    )
    shopping_cart = models.ForeignKey(to=ShoppingCart, on_delete=models.PROTECT, related_name='order')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    pay_choices = models.CharField(choices=PAY_CHOICES, max_length=15, default=1)
    activate_order_code = models.CharField(max_length=100, blank=True)
    order_comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    @staticmethod
    def generate_activation_code(length: int, number_range: str):
        from django.utils.crypto import get_random_string
        return get_random_string(length, number_range)

    def save(self, *args, **kwargs):
        self.activate_code = self.generate_activation_code(10, "qwerty123456789")
        return super().save(*args, **kwargs)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='items')

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f'OrderId: {self.order.id}, i{self.product.title}'

    def get_cost(self):
        return self.quantity * self.product.price