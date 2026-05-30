from django.db import models
from django.conf import settings
# Create your models here.

class OriginCountry(models.Model):
    name=models.CharField(max_length=100, unique=True)
    
    code=models.CharField(max_length=10, unique=True)

    is_activate=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    

class MalaisianCity(models.Model):
    name=models.CharField(max_length=100, unique=True)

    delivery_price=models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    
    estimation_delivery_days=models.IntegerField(default=1)

    is_activate=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Notification(models.Model):
    user= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    
    title=models.CharField(max_length=255)

    message=models.TextField()

    is_read=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering=["-created_at"]

    def __str__(self):
        return self.title
    