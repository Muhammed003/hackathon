from django.conf import settings
from django.db import models

from django.contrib.auth import get_user_model
from apps.category.models import Category


class Product(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # watch = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        return self.images.first()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.image.url


class Review(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self) -> str:
        return f"{self.author.email}"


class LikeProduct(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=False)


class SimilarProduct(models.Model):
    on_product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name="on_products")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name="products")


class Favorite(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)