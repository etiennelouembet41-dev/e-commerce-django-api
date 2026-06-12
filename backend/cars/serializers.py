from rest_framework import serializers
from .models import Car, CarImage


class CarImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ("id", "image", "created_at")


class CarSerializers(serializers.ModelSerializer):
    origin_country_name = serializers.SerializerMethodField()
    origin_country_code = serializers.SerializerMethodField()

    race_type_label = serializers.CharField(source="get_race_type_display", read_only=True)
    conditions_label = serializers.CharField(source="get_conditions_display", read_only=True)
    transmission_label = serializers.CharField(source="get_transmission_display", read_only=True)
    fuel_label = serializers.CharField(source="get_fuel_display", read_only=True)

    gallery = CarImageSerializers(many=True, read_only=True)

    class Meta:
        model = Car
        fields = (
            "id", "brand", "model", "year", "price",
            "origin_country", "origin_country_name", "origin_country_code",
            "race_type", "race_type_label",
            "power_hp", "mileage",
            "conditions", "conditions_label",
            "transmission", "transmission_label",
            "fuel", "fuel_label",
            "description", "main_image", "gallery",
            "is_available", "is_reserved", "is_sold",
            "created_at", "updated_at",
        )

    def get_origin_country_name(self, obj):
        return obj.origin_country.country.name if obj.origin_country else None

    def get_origin_country_code(self, obj):
        return str(obj.origin_country.country) if obj.origin_country else None