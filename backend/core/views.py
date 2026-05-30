from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import OriginCountry,MalaisianCity,Notification
from .serializers import OriginCountrySerializers,MalaisianCitySerializers,NotificationSerializer
# Create your views here.

class OriginCountryViewsets(viewsets.ModelViewSet):
    queryset=OriginCountry.objects.all()
    serializer_class=OriginCountrySerializers
    
class MalaisianCityViewsets(viewsets.ModelViewSet):
    queryset=MalaisianCity.objects.all()
    serializer_class=MalaisianCitySerializers
    
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class=NotificationSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

