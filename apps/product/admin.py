from django.contrib import admin
from .models import *
# Register your models here.


class ImageInLineAdmin(admin.TabularInline):
    model = ProductImage
    fields = ('image',)
    max_num = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInLineAdmin, ]


admin.site.register(LikeProduct)
admin.site.register(ProductImage)
