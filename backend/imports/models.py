from django.db import models
from cars.models import Car


class ImportInfo(models.Model):

    IMPORT_STATUS_CHOICES = (
        ("pending", "En attente"),
        ("confirmed", "Confirmé"),
        ("supplier_purchase", "Achat fournisseur"),
        ("documents_preparation", "Documents en préparation"),
        ("international_shipping", "Expédition internationale"),
        ("malaysia_customs", "Douane Malaisie"),
        ("local_delivery", "Livraison locale"),
        ("delivered", "Livré"),
    )

    car = models.OneToOneField(
        Car,
        on_delete=models.CASCADE,
        related_name="import_info"
    )

    estimated_import_cost = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_import_days = models.PositiveIntegerField()
    required_documents = models.TextField()
    customs_fees = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=50,
        choices=IMPORT_STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        old_status = None

        if self.pk:
            old_status = ImportInfo.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        if old_status and old_status != self.status:
            from core.models import Notification

            for order in self.car.orders.all():
                Notification.objects.create(
                    user=order.user,
                    title="Mise à jour importation",
                    message=(
                        f"Le statut d'importation de votre commande "
                        f"#{order.id} est maintenant : {self.get_status_display()}."
                    )
                )

    def __str__(self):
        return f"Import info - {self.car}"