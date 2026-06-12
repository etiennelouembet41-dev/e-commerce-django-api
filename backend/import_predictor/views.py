from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from cars.models import Car
from core.models import MalaisianCity
from .services import predict_import_cost


class ImportCostPredictionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        car_id = request.data.get("car_id")
        city_id = request.data.get("city_id")

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        delivery_city = None

        if city_id:
            try:
                delivery_city = MalaisianCity.objects.get(id=city_id)
            except MalaisianCity.DoesNotExist:
                return Response({"error": "City not found"}, status=404)

        prediction = predict_import_cost(car, delivery_city)

        if not prediction:
            return Response(
                {"error": "No import rule found for this country"},
                status=404
            )

        return Response(prediction)