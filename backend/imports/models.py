from django.db import models
from cars.models import Car
# Create your models here.

class ImportInfo(models.Model):
    
    IMPORT_STATUS_CHOICES=(
        ("pending","Pending"),
        ("confirmed", "Confirmed"),
        ("supplier_purchase", "Supplier Purchase"),
        ("documents_preparation", "documents in preparation"),
        ("international_shipping", "International Shipping"),
        ("malaysia_customs","Malaysian Customs"),
        ("local_delivery", "Local Delivery"),
        ("delivered","Delivered"),
        
    )
    
    car=models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="import_info",
    )
    
    estimated_import_cost=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    estimated_import_days=models.PositiveIntegerField()

    required_documents=models.TextField()

    customs_fees =models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    
    status=models.CharField(
        max_length=50,
        choices=IMPORT_STATUS_CHOICES,
        default="pending",
    )
    
    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Import Info - {self.car}"
    
    

    
    