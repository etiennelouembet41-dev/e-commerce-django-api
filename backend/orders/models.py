from django.db import models
from django.conf import settings
from cars.models import Car
from core.models import MalaisianCity
from addresses.models import Address
# Create your models here.

class Order(models.Model):
    OREDER_STATUS_CHOICES=(
        ("pending","Pending"),
        ("confirmed","Confirmed"),
        ("processing","Processing"),
        ("importing","import in progress"),
        ("delivering","Delivering in progress"),
        ("completed","Completed"),
        ("cancelled","Cancelled"),
    )
    
    PAYMENT_STATUS_CHOICES=(
        ("unpaid","Non payé"),
        ("deposit_paid","Acompte payé"),
        ("paid","Payé"),
        ("failed","Echec Paiement"),
        ("refunded","Remboursé"),
    )
    
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    
    car=models.ForeignKey(
        Car,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    
    delivery_city=models.ForeignKey(
        MalaisianCity,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    
    delivery_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    
    car_price=models.DecimalField(max_digits=12,decimal_places=2)

    import_fees=models.DecimalField(max_digits=12,decimal_places=2)

    delivery_fees=models.DecimalField(max_digits=12,decimal_places=2)

    total_price=models.DecimalField(max_digits=12, decimal_places=2)

    status=models.CharField(
        max_length=50,
        choices=OREDER_STATUS_CHOICES,
        default="pending",
        
    )
    
    payment_status=models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default="unpaid",
    )
    
    stripe_payment_id=models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    
    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):
    
    orders=models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    
    car=models.ForeignKey(
        Car,
        on_delete=models.PROTECT
    )
    
    quantity=models.PositiveIntegerField(default=1)

    price=models.DecimalField(max_digits=12,decimal_places=2)

    def __str__(self):
        return f"{self.car} x {self.quantity}"
    
    
    
