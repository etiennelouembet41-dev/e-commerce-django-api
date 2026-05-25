from django.contrib import admin
from .models import ImportInfo


@admin.register(ImportInfo)
class ImportInfoAdmin(admin.ModelAdmin):
    list_display = (
        "car",
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