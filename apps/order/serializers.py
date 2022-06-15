from apps.order.models import Order, OrderItem
from rest_framework import serializers


class OrdersSerializer(serializers.ModelSerializer):
    order_comments = serializers.CharField(required=False)
    email = serializers.SerializerMethodField('_user')

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            print(request.user)
            return request.user

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ordered_products'] = OrdersHistorySerializer(instance.items.all(),
                                                  many=True, context=self.context).data
        return representation


class OrdersHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('quantity', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = instance.product.title
        print(instance.product)
        representation['total_price'] = instance.get_cost()
        return representation

