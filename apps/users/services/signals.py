from apps.cart.models import ShoppingCart


def post_create_cart_signal(sender, instance, created, *args, **kwargs):
    if created:
        ShoppingCart.objects.create(user=instance)

