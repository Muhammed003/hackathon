from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from .views import *

urlpatterns = [
    # login sing_up
    path('api/register/', RegistrationView.as_view(), name='hello'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("activate/<str:activate_code>/", ActivateView.as_view()),

    # forgot rest password
    path('forgot-password/', ForgetPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view(), name="register"),
    path('subscribe/', SubscribeView.as_view(), name="subscribe"),
]