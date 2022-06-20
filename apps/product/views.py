from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
import django_filters.rest_framework as filters
from rest_framework.decorators import action

from ..tasks.tasks import send_notification_message_task
from ..users.models import CustomUser


"""                     My models                       """

from .paginations import ProductPagination
from ..users.permissions import IsAdminOrAllowAny, IsReviewAuthor
from .models import Product, Review, LikeProduct, Favorite
from .serializers import ProductSerializer, ReviewProductSerializer, ProductDetailSerializer, \
    FavoriteListSerializer

"""             Serializers                 """

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ['create_date', 'name', 'price', 'type']
    permission_classes = [IsAuthenticated, ]
    pagination_class = ProductPagination
    search_fields = ['name', 'description']

    @method_decorator(cache_page(60 * 15))
    def list(self, request, format=None):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['toggle_like', ]:
            return [IsAuthenticated()]
        return []

    # products/id/like/
    @action(detail=True, methods=['GET'])
    def toggle_like(self, request, pk):
        product = self.get_object()
        user = request.user
        fav, created = LikeProduct.objects.get_or_create(product=product, user=user)
        if fav.is_like == False:
            fav.is_like = not fav.is_like
            fav.save()
            return Response('You liked this product')
        else:
            fav.is_like = not fav.is_like
            fav.save()
            return Response('You disliked this product')

    # product/id/favorite/
    @action(detail=True, methods=['GET'])
    def favorite(self, request, pk):
        product = self.get_object()
        user = request.user
        fav, created = Favorite.objects.get_or_create(product=product, user=user)
        if fav.favorite == False:
            fav.favorite = not fav.favorite
            fav.save()
            return Response('Added to Favs')
        else:
            fav.favorite = not fav.favorite
            fav.save()
            return Response('Not in Favs')

    def create(self, request, **validated_data):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        product_name = serializer.data.get('name')
        product_id = serializer.data.get('id')
        # for contact in CustomUser.objects.filter(is_subscribed=True):
        #     send_notification_message_task(contact.email, product_name, product_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        def perform_create(self, serializer):
            serializer.save()

class ReviewProductView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewProductSerializer
    permission_classes = [IsReviewAuthor, IsAuthenticatedOrReadOnly]


class ProductDetailView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class FavoriteView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        #                           model     FK                      model     boolean_field
        queryset = queryset.filter(favorites__user=self.request.user, favorites__favorite=True)
        return queryset


"""                  END            Serializers                 """

