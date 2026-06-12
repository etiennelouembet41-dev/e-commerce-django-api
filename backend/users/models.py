from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES=(
        ("customer","Customer"),
        ("manager","Manager"),
        ("admin","Admin"),
    )
    
    GENDER_CHOICES=(
        ("male","Male"),
        ("female","Female"),
    )
    
    email=models.EmailField(unique=True)
    
    phone_number=models.CharField(max_length=20, blank=True)
    
    profile_image=models.ImageField(
        upload_to="users/profiles/",
        blank=True,
        null=True,
    )
    
    country=models.CharField(max_length=200, blank=True)
    
    city=models.CharField(max_length=100, blank=True)
    
    stripe_customer_id=models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    
    role=models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer",
    )
    
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    
    nationality = CountryField(
        blank=False,
        null=False
    )
    
    is_verified=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    upload_at=models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD="email"
    
    REQUIRED_FIELDS=["username"]
    
    def __str__(self):
        return self.email
    
    
    
    
    
    
