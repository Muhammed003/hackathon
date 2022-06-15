from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *

# router = SimpleRouter()
# router.register('', OrderViewSet)

urlpatterns = [
    path("", OrderViewSet.as_view()),
    path("confirm/<str:activate_code>", ActivateOrderView.as_view()),
    # path("history/", OrderHistoryView.as_view()),

]

