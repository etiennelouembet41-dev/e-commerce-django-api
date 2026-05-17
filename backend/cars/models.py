from django.db import models
from core.models import OriginCountry
# Create your models here.


class Car(models.Model):
    
    RACE_TYPE_CHOICES=(
        ("circuit","Circuit"),
        ("drift","Drift"),
        ("rally","Rally"),
        ("drag","Drag Race"),
        ("amateur","Compétition amateur"),
        ("f1", "Formula 1"),
        ("gt", "GT Racing"),
        ("endurance", "Endurance"),
        ("touring", "Touring Car"),
        ("motogp", "Moto GP"),
        ("superbike", "Superbike"),
        ("offroad", "Off Road"),
        ("indycar", "IndyCar Series"),
        ("formuleE","Formule E"),
        ("hypercars","Hypercars / Prototypes"),
        
    )
    
    CONDITIONS_CHOICES=(
        ("excellent","Excellent"),
        ("good","Good"),
        ("fair","Fair"),
        ("needs_work","Needs Work"),
    )
    
    TRANSMISSION_CHOICES=(
        ("manual","Manual"),
        ("automatic","Automatic"),
        ("sequential","Sequential"),
    )
    
    FUEL_CHOICES=(
        ("petrol","Petrol"),
        ("hybrid","Hybrid"),
        ("diesel","Diesel"),
        ("electric","Electric"),
    )
    
    brand=models.CharField(max_length=100)

    model=models.CharField(max_length=100)

    year=models.PositiveBigIntegerField()

    price=models.DecimalField(max_digits=10, decimal_places=2)

    origin_country=models.ForeignKey(
        OriginCountry,
        on_delete=models.CASCADE,
        related_name="cars"
    )
    
    race_type=models.CharField(
        max_length=50,
        choices=RACE_TYPE_CHOICES
    )
    
    power_hp=models.PositiveBigIntegerField()

    mileage=models.PositiveBigIntegerField(help_text="Mileage en km")

    conditions=models.CharField(
        max_length=50,
        choices=CONDITIONS_CHOICES
    )
    
    transmission=models.CharField(
        max_length=50,
        choices=TRANSMISSION_CHOICES,
    )
    
    description=models.TextField()

    main_image=models.ImageField(
        upload_to="cars/main/",
        blank=True,
        null=True,
    )
    
    is_available=models.BooleanField(default=True)

    is_reserved=models.BooleanField(default=False)

    is_sold=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class CarImage(models.Model):
    car=models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="gallery"
    )
    
    image=models.ImageField(
        upload_to="cars/gallery/",
        
    )
    
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image - {self.car}"