from django.urls import path

from .views import ShoppingCartView, AddProductInCartView

urlpatterns = [
    path('', ShoppingCartView.as_view()),
    path('<int:pk>/', ShoppingCartView.as_view()),
    path('add/', AddProductInCartView.as_view()),
]