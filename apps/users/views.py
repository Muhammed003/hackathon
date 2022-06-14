from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer
from .services.utils import send_activation_code


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_code(user.activate_code, user.email)
            message = "You are successfully registrated, we have sent activation code to your email! Thank you!"

            return Response(message)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class ActivateView(APIView):
    def get(self, request, activate_code):
        user = get_object_or_404(CustomUser, activate_code=activate_code)
        user.is_active = True
        user.activate_code = ''
        user.save()
        return Response('Your Account is successfully activated!', status=status.HTTP_200_OK)
