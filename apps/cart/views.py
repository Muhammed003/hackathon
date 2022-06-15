from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from .models import ShoppingCart
from .serializers import *
from drf_yasg.utils import swagger_auto_schema


class ShoppingCartView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        cart = user.cart
        serializer = CartSerializers(cart)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CartSerializers)
    def put(self, request, pk=None):
        cart = request.user.cart
        try:
            cart_item: CartItem = cart.cart_item.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"message": "No pk with that number"}, status=status.HTTP_204_NO_CONTENT)

        quantity = request.data.get("quantity")
        cart_item.quantity = int(quantity)
        cart_item.save()
        serializer = CartItemSerializers(cart_item)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CartSerializers)
    def delete(self, request, pk=None):
        cart = request.user.cart
        try:
            cart_item: CartItem = cart.cart_item.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"message": "not is object"}, status=status.HTTP_204_NO_CONTENT)

        cart_item.delete()
        return Response(status=status.HTTP_200_OK)


class AddProductCartView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=CartItemSerializers)
    def post(self, request):
        data = request.POST
        serializer = CartItemSerializers(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


