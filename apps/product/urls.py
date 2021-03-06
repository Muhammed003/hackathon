from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('reviews', ReviewProductView)
router.register('', ProductViewSet)
urlpatterns = [
    # """                  Start            Serializers                 """,
    # path("similars/", ProductDetailView.as_view()),
    path("", include(router.urls)),
    path("", include(router.urls)),
    # """                  End            Serializers                 """,


]
