from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from config import settings
from .models import Order, OrderItem
from .serializers import OrdersSerializer, OrdersHistorySerializer
from apps.cart.cart import Cart
from ..cart.models import CartItem
from ..product.models import Product
from ..users.models import CustomUser
from ..users.services.utils import send_order_activate_code


class OrderViewSet(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            posts = Order.objects.filter(user=request.user, paid=True)
            serializer = OrdersSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            return Response("You should log in to your account to start")

    @swagger_auto_schema(request_body=OrdersSerializer)
    def post(self, request):
        data = request.data
        serializer = OrdersSerializer(data=data, context={'request': request})
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except:
            raise serializers.ValidationError(
                'User was not found'
            )
        carts = CartItem.objects.filter(cart_shopping=user.cart)
        if serializer.is_valid(raise_exception=True):
            if carts.exists():
                order = serializer.save()
                activate_order = order.generate_activation_code(10, "qwerty12345")
                order.activate_order_code = activate_order
                order.email = request.user
                for cart in carts:
                    product = Product.objects.get(pk=int(cart.product_id))
                    OrderItem.objects.create(order=order,
                                             product=product,
                                             quantity=int(cart.quantity),
                                             price=product.price
                                             )
                order.save()
                send_order_activate_code(order.user.email, order.activate_order_code)
                return Response("Please confirm you order")
            else:
                return Response("Cart is empty")
        else:
            return Response("Error try again", status="fail")


class OrderHistoryView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrdersHistorySerializer(orders, many=True)
        return Response(serializer.data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Order.objects.filter(paid=True)
        return context

class ActivateOrderView(APIView):
    def get(self, request, activate_code):
        user = get_object_or_404(Order, activate_order_code=activate_code)
        user.paid = True
        user.activate_order_code = ''
        CartItem.objects.all().delete()
        user.save()
        return Response('Your successfully ordered! Thanks for your order we hope you enjoyed shopping with us', status=status.HTTP_200_OK)

# class AddProductCartView(APIView):
#     permission_classes = (IsAuthenticated, )
#
#     def post(self, request):
#         data = request.POST
#         serializer = OrderItemSerializer(data=data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

