from django.db import models
from django.conf import settings
from core.models import MalaisianCity
# Create your models here.

class Address(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses"
        
    )
    
    city=models.ForeignKey(
        MalaisianCity,
        on_delete=models.CASCADE,
    )
    
    address_line=models.TextField()

    postal_code=models.CharField(
        max_length=20,
        blank=True,
    )
    
    is_default=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}-{self.city.name}"


