from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth import get_user_model


class Product(models.Model):
    list_category = ['/dressers', '/hallways', '/tv-stand', '/living-room-sets',
                     '/kitchens',
                     '/children-sets']
    PRODUCT_CHOICES = (
        ("wardrobes", "ШКАФ"),
        ("bedroom-sets", "СПАЛЬНИ"),
        ("hallways", "ПРИХОЖИЕ"),
        ("kitchens", "КУХНИ"),
        ("tv-stand", "TV ТУМБЫ"),
        ("dressers", "КОМОДЫ"),
        ("living-room-sets", "ГОСТИНЫЕ"),
        ("children-sets", "ДЕТСКИЕ & ОФИС"),
        ("cushioned-furniture", "МЯГКАЯ МЕБЕЛЬ"),
    )

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=PRODUCT_CHOICES, max_length=255,  default="cupboard")
    manufacture = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Product {}'.format(self.id)

    @property
    def get_image(self):
        return self.images.first()


class Review(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1, verbose_name='Рейтинг')

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