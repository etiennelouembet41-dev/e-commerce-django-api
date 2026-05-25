from django.contrib import admin
from .models import OriginCountry,MalaisianCity
# Register your models here.
 
 
@admin.register(OriginCountry)
class OriginCountryAdmin(admin.ModelAdmin):
    list_display=(
        "name",
        "code",
        "is_activate",
        "created_at",
    )
    
    list_filter=(
        "is_activate",
    )
    
    search_fields=( 
        "name",
        "code",
    )
    
@admin.register(MalaisianCity)
class MalaisianCityAdmin(admin.ModelAdmin):
    list_display=(
        "name",
        "delivery_price",
        "estimation_delivery_days",
        "is_activate",
    )
    
    list_filter=(
        "is_activate",
    )
    
    search_fields=(
        "name",
    )