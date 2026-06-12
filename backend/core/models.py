from django.db import models
from django_countries.fields import CountryField
from django.conf import settings


class OriginCountry(models.Model):
    country = CountryField(unique=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pays d'origine"
        verbose_name_plural = "Pays d'origine"

    def __str__(self):
        return self.country.name
    
    

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

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ("user_registered", "Utilisateur inscrit"),
        ("order_created", "Commande créée"),
        ("payment_confirmed", "Paiement confirmé"),
        ("car_created", "Voiture ajoutée"),
        ("car_updated", "Voiture modifiée"),
        ("car_deleted", "Voiture supprimée"),
        ("import_status_updated", "Statut import modifié"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )

    action = models.CharField(max_length=100, choices=ACTION_CHOICES)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.created_at}"