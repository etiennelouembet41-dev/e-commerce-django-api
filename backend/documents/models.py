from django.db import models
from orders.models import Order
from django.conf import settings


class Document(models.Model):

    DOCUMENT_STATUS = [
        ("pending", "En attente"),
        ("approved", "Validé"),
        ("rejected", "Rejeté"),
    ]


    DOCUMENT_TYPES = [
        ("invoice", "Facture"),
        ("contract", "Contrat"),
        ("passport", "Passeport"),
        ("id_card", "Carte identité"),
        ("customs", "Document douanier"),
        ("registration", "Immatriculation"),
        ("vehicle_photo", "Photo véhicule"),
        ("other", "Autre"),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES
    )

    file = models.FileField(
        upload_to="documents/"
    )
    
    status = models.CharField(
        max_length=20,
        choices=DOCUMENT_STATUS,
        default="pending"
    )

    uploaded_by_admin = models.BooleanField(
        default=False
    )

    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_documents"
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    rejection_reason = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.document_type} - Order {self.order_id}"