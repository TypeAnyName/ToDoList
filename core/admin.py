from django.contrib import admin

from core.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', "first_name", 'last_name',)
    search_fields = ('email', 'first_name', "last_name", "username",)
    list_filter = ('is_staff', "is_active", "is_superuser",)
