from django.urls import path
from .views import *

urlpatterns = [
    path('furniture/', ParseProductView.as_view()),
    path('furniture/add/', ParsingCreateView.as_view()),
]