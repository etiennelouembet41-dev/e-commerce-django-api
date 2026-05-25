from django.contrib import admin
from .models import Car,CarImage
# Register your models here.


class CarImageInline(admin.TabularInline):
    model=CarImage
    extra=1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines=[CarImageInline]
    
    list_display = (
        "brand",
        "model",
        "year",
        "price",
        "origin_country",
        "race_type",
        "power_hp",
        "is_available",
        "is_reserved",
        "is_sold",
    )
    
    list_filter = (
        "brand",
        "origin_country",
        "race_type",
        "conditions",
        "transmission",
        "fuel",
        "is_available",
        "is_reserved",
        "is_sold",
    )

    search_fields = (
        "brand",
        "model",
        "description",
    )

    ordering = ("-created_at",)


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ("car", "created_at")
    search_fields = ("car__brand", "car__model")