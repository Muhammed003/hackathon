from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
# Create your views here.
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import Token

from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .services.utils import send_activation_code, send_new_password


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_code(user.activate_code, user.email)
            message = "You are successfully registrated, we have sent activation code to your email! Thank you!"

            return Response(message, status=status.HTTP_200_OK)


class ActivateView(APIView):
    def get(self, request, activate_code):
        user = get_object_or_404(CustomUser, activate_code=activate_code)
        user.is_active = True
        user.save()
        return Response('Your Account is successfully activated!', status=status.HTTP_200_OK)


class ForgetPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            user: CustomUser = CustomUser.objects.get(email=email)
            new_token_to_password = user.generate_activation_code(10, "qwerty12345")
            user.activate_code = new_token_to_password
            user.save()
            send_new_password(email, user.activate_code)

            return Response({"message": "We send you code to change password"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Error email"})


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        data = request.POST
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get("password")
            activate_code = serializer.validated_data.get("activate_code")
            try:
                user = CustomUser.objects.get(activate_code=activate_code)
                if activate_code == user.activate_code:
                        password = serializer.validated_data.get('password')
                        user.activate_code = ''
                        user.set_password(password)
                        user.save()
                        return Response({'message': "Your password successfully changed"}, status=status.HTTP_200_OK)
            except:
                return Response({'message':"Incorrect activation code"}, status=status.HTTP_401_UNAUTHORIZED)

# SUBSCRIBE


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        user = CustomUser.objects.get(pk=request.user.id)
        if user.is_subscribed == False:
            user.is_subscribed = not user.is_subscribed
            user.save()
            return Response('You subscribed to our products. Thank you !!!')
        else:
            user.is_subscribed = not user.is_subscribed
            user.save()
            return Response("You unsubscribed you can't get notification.")
# product = self.get_object()
# user = request.user
# fav, created = LikeProduct.objects.get_or_create(product=product, user=user)
# if fav.is_like == False:
#     fav.is_like = not fav.is_like
#     fav.save()
#     return Response('You liked this product')
# else:
#     fav.is_like = not fav.is_like
#     fav.save()
#     return Response('You disliked this product')
