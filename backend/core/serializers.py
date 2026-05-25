from rest_framework import serializers 
from .models import OriginCountry,MalaisianCity

class OriginCountrySerializers(serializers.ModelSerializer):
    class Meta:
        model=OriginCountry
        fields="__all__"

class MalaisianCitySerializers(serializers.ModelSerializer):
    class Meta:
        model=MalaisianCity
        fields="__all__"