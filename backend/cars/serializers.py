from rest_framework import serializers
from .models import Car,CarImage

class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model=Car
        fields="__all__"

class CarImageSerializers(serializers.ModelSerializer):
    class Meta:
        model=CarImage
        fields=("id","image","created_at",)