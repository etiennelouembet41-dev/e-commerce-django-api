from rest_framework import serializers
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = (
            "id",
            "invoice_number",
            "payment_type",
            "amount_paid",
            "pdf_url",
            "created_at",
        )

    def get_pdf_url(self, obj):
        request = self.context.get("request")

        if obj.pdf_file:
            url = obj.pdf_file.url
            if request:
                return request.build_absolute_uri(url)
            return url

        return None