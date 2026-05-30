
from django.core.management.base import BaseCommand
from core.models import OriginCountry, MalaisianCity
from cars.models import Car
from imports.models import ImportInfo


class Command(BaseCommand):
    help = "Seed database with countries, Malaysian cities, cars and import info"

    def handle(self, *args, **kwargs):
        japan, _ = OriginCountry.objects.get_or_create(name="Japon", code="JP")
        germany, _ = OriginCountry.objects.get_or_create(name="Allemagne", code="DE")
        uk, _ = OriginCountry.objects.get_or_create(name="Royaume-Uni", code="UK")
        usa, _ = OriginCountry.objects.get_or_create(name="États-Unis", code="US")

        cities = [
            ("Kuala Lumpur", 800, 3),
            ("Johor Bahru", 1200, 5),
            ("Penang", 1000, 4),
            ("Malacca", 900, 3),
            ("Ipoh", 950, 4),
        ]

        for name, price, days in cities:
            MalaisianCity.objects.get_or_create(
                name=name,
                defaults={
                    "delivery_price": price,
                    "estimation_delivery_days": days,
                }
            )

        cars = [
            {
                "brand": "Nissan",
                "model": "Skyline GT-R R34",
                "year": 2002,
                "price": 450000,
                "origin_country": japan,
                "race_type": "circuit",
                "power_hp": 500,
                "mileage": 80000,
                "conditions": "excellent",
                "transmission": "manual",
                "fuel": "petrol",
                "description": "Voiture iconique japonaise préparée pour circuit.",
                "import_cost": 35000,
                "import_days": 45,
                "customs_fees": 18000,
            },
            {
                "brand": "Nissan",
                "model": "Silvia S15",
                "year": 2001,
                "price": 180000,
                "origin_country": japan,
                "race_type": "drift",
                "power_hp": 380,
                "mileage": 95000,
                "conditions": "good",
                "transmission": "manual",
                "fuel": "petrol",
                "description": "Excellent choix pour drift amateur et semi-pro.",
                "import_cost": 28000,
                "import_days": 40,
                "customs_fees": 12000,
            },
            {
                "brand": "Toyota",
                "model": "Supra MK4",
                "year": 1998,
                "price": 380000,
                "origin_country": japan,
                "race_type": "drag",
                "power_hp": 650,
                "mileage": 70000,
                "conditions": "excellent",
                "transmission": "manual",
                "fuel": "petrol",
                "description": "Supra préparée pour accélération et performance.",
                "import_cost": 33000,
                "import_days": 45,
                "customs_fees": 16000,
            },
            {
                "brand": "BMW",
                "model": "M3 E46",
                "year": 2004,
                "price": 220000,
                "origin_country": germany,
                "race_type": "circuit",
                "power_hp": 360,
                "mileage": 110000,
                "conditions": "good",
                "transmission": "manual",
                "fuel": "petrol",
                "description": "Base solide pour track day et compétition amateur.",
                "import_cost": 30000,
                "import_days": 50,
                "customs_fees": 14000,
            },
            {
                "brand": "Ford",
                "model": "Mustang GT",
                "year": 2016,
                "price": 260000,
                "origin_country": usa,
                "race_type": "drag",
                "power_hp": 460,
                "mileage": 60000,
                "conditions": "good",
                "transmission": "manual",
                "fuel": "petrol",
                "description": "Muscle car puissante pour drag race.",
                "import_cost": 40000,
                "import_days": 60,
                "customs_fees": 20000,
            },
        ]

        for data in cars:
            import_cost = data.pop("import_cost")
            import_days = data.pop("import_days")
            customs_fees = data.pop("customs_fees")

            car, _ = Car.objects.get_or_create(
                brand=data["brand"],
                model=data["model"],
                year=data["year"],
                defaults=data
            )

            ImportInfo.objects.get_or_create(
                car=car,
                defaults={
                    "estimated_import_cost": import_cost,
                    "estimated_import_days": import_days,
                    "required_documents": "Invoice, Export Certificate, Bill of Lading, Customs Form",
                    "customs_fees": customs_fees,
                    "status": "pending",
                }
            )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))