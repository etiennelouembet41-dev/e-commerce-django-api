from django.db import models
from core.models import OriginCountry


class ImportCostRule(models.Model):
    origin_country = models.ForeignKey(
        OriginCountry,
        on_delete=models.CASCADE,
        related_name="import_cost_rules"
    )

    base_shipping_cost = models.DecimalField(max_digits=12, decimal_places=2)
    customs_rate = models.DecimalField(max_digits=5, decimal_places=2)
    insurance_rate = models.DecimalField(max_digits=5, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=12, decimal_places=2)

    estimated_days = models.PositiveIntegerField(default=45)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Import rule - {self.origin_country.country.name}"