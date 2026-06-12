from django.contrib import admin
from .models import OriginCountry,MalaisianCity,AuditLog
# Register your models here.
 
 
@admin.register(OriginCountry)
class OriginCountryAdmin(admin.ModelAdmin):
    list_display=(
        
        "country",
        "is_active",
        "created_at",
    )
    
    list_filter=(
        "is_active",
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

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("message", "user__email")
    readonly_fields = ("user", "action", "message", "created_at")