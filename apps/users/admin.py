from django.contrib import admin

# Register your models here.
from apps.users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'email', 'is_active', 'date_joined']
    list_filter = ['is_active', 'date_joined']


admin.site.register(CustomUser, UserAdmin)
