from django.contrib import admin
from .models import ImportCostRule


@admin.register(ImportCostRule)
class ImportCostRuleAdmin(admin.ModelAdmin):
    list_display = (
        "origin_country",
        "base_shipping_cost",
        "customs_rate",
        "insurance_rate",
        "processing_fee",
        "estimated_days",
        "is_active",
    )

    list_filter = ("origin_country", "is_active")