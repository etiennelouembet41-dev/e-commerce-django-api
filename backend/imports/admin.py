from django.contrib import admin
from .models import ImportInfo


@admin.register(ImportInfo)
class ImportInfoAdmin(admin.ModelAdmin):
    list_display = (
        "car",
        "get_order_id",
        "get_customer",
        "estimated_import_cost",
        "customs_fees",
        "estimated_import_days",
        "status",
        "updated_at",
    )

    list_filter = ("status",)

    search_fields = (
        "car__brand",
        "car__model",
        "required_documents",
    )

    def get_order_id(self, obj):
        order = obj.car.orders.first()
        return order.id if order else "-"

    get_order_id.short_description = "Commande"

    def get_customer(self, obj):
        order = obj.car.orders.first()
        return order.user.email if order else "-"

    get_customer.short_description = "Client"