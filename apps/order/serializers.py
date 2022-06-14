from rest_framework import serializers

from .models import CartItem, ShoppingCart


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')

    def validate(self, attrs):
        cart_shopping = self.context.get("request").user.cart
        attrs['cart_shopping'] = cart_shopping
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep['product'] = instance.product.name
            rep['total_price'] = instance.get_total_price_item()
            return rep
        except:
            return rep 


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep['products'] = CartItemSerializer(instance.cart_item.all(), many=True).data
            rep['total_price'] = instance.get_total_all_price()
            return rep
        except:
            return rep 