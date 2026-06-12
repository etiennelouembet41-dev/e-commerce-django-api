from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "order",
        "payment_type",
        "amount_paid",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "order__user__email",
    )

    list_filter = (
        "payment_type",
        "created_at",
    )

    readonly_fields = (
        "invoice_number",
        "created_at",
        "pdf_file",
    )