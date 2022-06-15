from django.urls import path

from .views import ShoppingCartView, AddProductCartView
urlpatterns = [
    path('', ShoppingCartView.as_view()),
    path('<int:pk>/', ShoppingCartView.as_view()),
    path('add/', AddProductCartView.as_view()),
]