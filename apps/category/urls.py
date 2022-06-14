from django.urls import path

from .views import *

#может быть нужны будут изменения
urlpatterns = [
    path('', CategoryView.as_view()),
    path('create/', CategoryCreateView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
    path('delete/<int:pk>/', CategoryDeleteView.as_view()),
    path('update/<int:pk>/', CategoryUpdateView.as_view()),

]
