import django_filters.rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.parse.paginations import ParsePaginations
from apps.parse.parsing import DATA
from apps.parse.serializers import ParseProductSerializer
from ..product.models import Product
from rest_framework.views import APIView
from apps.users.models import CustomUser
from rest_framework.response import Response
from rest_framework import status


class ParseProductView(generics.ListAPIView):
    queryset = DATA
    serializer_class = ParseProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = ParsePaginations


class ParsingCreateView(APIView):
    def get(self, request):
        product = Product.objects.all()
        for item in DATA:
            obj, created = Product.objects.get_or_create(name=item.get('title'),
                                   author= CustomUser.objects.get(pk=1),
                                   description=item.get('description'),
                                   price=int(item.get('price')),
                                   type=item.get('type'),
                                   manufacture=item.get('manufacture'),
                                     )
        return Response("Saved", status=status.HTTP_200_OK)