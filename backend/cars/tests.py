from django.test import TestCase
from core.models import OriginCountry
from cars.models import Car


class CarModelTest(TestCase):

    def test_create_car(self):
        country = OriginCountry.objects.create(
            name="Japon",
            code="JP"
        )

        car = Car.objects.create(
            brand="Nissan",
            model="Silvia S15",
            year=2001,
            price=180000,
            origin_country=country,
            race_type="drift",
            power_hp=380,
            mileage=95000,
            condition="good",
            transmission="manual",
            fuel="petrol",
            description="Test car"
        )
        
        response = self.client.get("/api/cars/")

        self.assertEqual(str(car), "Nissan Silvia S15 (2001)")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)