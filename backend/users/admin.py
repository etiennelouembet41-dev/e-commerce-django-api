from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

@admin.register(User)
class CustomerUserAdmin(UserAdmin):
    list_display=(
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    )
    
    list_filter=(
        "role",
        "is_staff",
        "is_active",
    )
    
    search_fields=(
        "email",
        "username",
        "first_name",
        "last_name",
        
    )
    
    ordering=("email",)