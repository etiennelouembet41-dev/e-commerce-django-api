from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    list_display = (
        "id",
        "user",
        "car",
        "delivery_city",
        "total_price",
        "status",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "delivery_city",
        "created_at",
    )

    search_fields = (
        "user__email",
        "car__brand",
        "car__model",
        "stripe_payment_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin): 
    list_display = ("id","orders", "car", "quantity", "price",)
    search_fields = ("car__brand", "car__model",)