from rest_framework import serializers 
from .models import OriginCountry,MalaisianCity,Notification

class OriginCountrySerializers(serializers.ModelSerializer):
    class Meta:
        model=OriginCountry
        fields="__all__"

class MalaisianCitySerializers(serializers.ModelSerializer):
    class Meta:
        model=MalaisianCity
        fields="__all__"
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields="__all__"