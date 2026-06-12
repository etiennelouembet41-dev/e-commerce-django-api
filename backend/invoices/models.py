from django.db import models
from orders.models import Order


class Invoice(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ("deposit_20", "Acompte 20%"),
        ("remaining", "Restant 80%"),
        ("full", "Paiement total"),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    invoice_number = models.CharField(max_length=100, unique=True)

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES
    )

    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)

    pdf_file = models.FileField(
        upload_to="invoices/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number