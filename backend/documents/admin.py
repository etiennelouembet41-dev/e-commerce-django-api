from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "document_type",
        "status",
        "uploaded_by_admin",
        "validated_by",
        "validated_at",
        "created_at",
    )

    list_filter = (
        "document_type",
        "status",
        "uploaded_by_admin",
        "created_at",
    )

    search_fields = (
        "order__id",
        "order__user__email",
        "rejection_reason",
    )

    readonly_fields = (
        "created_at",
        "validated_at",
    )