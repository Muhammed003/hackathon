from rest_framework import serializers
from .models import Product, ProductImage, Review, LikeProduct, SimilarProduct


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Product
        exclude = ('create_date', 'update_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['category'] = instance.category.name
        representation['author'] = instance.author.email
        representation['images'] = ProductImageSerializer(instance.images.all(),
                                                  many=True, context=self.context).data
        representation['reviews'] = ReviewProductSerializer(instance.reviews.all(),
                                                  many=True, context=self.context).data

        representation['likes'] = instance.likes.filter(is_like=True).count()
        # instance.likes.get(is_like=True)
        if instance.likes.filter(is_like=True, user_id=self.context['request'].user.id):
            representation['liked_by_user'] = True
        else:
            representation['liked_by_user'] = False
        return representation


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')

            if request is not None:
                url = request.build_absolute_uri(url)

        else:
            url = ''

        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['product'] = instance.product.name
        return representation


class ReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('author', )

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['product'] = instance.product.name
        return representation


class LikeProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeProduct
        fields = "__all__"


class SimilarProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = SimilarProduct
        fields = ['category', 'price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = instance.product.name
        return representation


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    products = SimilarProductSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'