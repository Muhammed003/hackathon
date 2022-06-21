from django.contrib import admin
from .models import *
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price', 'author', 'type', 'manufacture']
    list_filter = ['price', ]
    search_fields = ['name']


admin.site.register(LikeProduct)
admin.site.register(Product, ProductAdmin)
