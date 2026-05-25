from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "city",
        "postal_code",
        "is_default",
        "created_at",
    )
    list_filter = ("city", "is_default")
    search_fields = ("user__email", "address_line", "postal_code")
