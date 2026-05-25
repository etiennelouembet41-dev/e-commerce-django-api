from django.shortcuts import render
from rest_framework import viewsets
from .models import OriginCountry,MalaisianCity
from .serializers import OriginCountrySerializers,MalaisianCitySerializers
# Create your views here.

class OriginCountryViewsets(viewsets.ModelViewSet):
    queryset=OriginCountry.objects.all()
    serializer_class=OriginCountrySerializers
    
class MalaisianCityViewsets(viewsets.ModelViewSet):
    queryset=MalaisianCity.objects.all()
    serializer_class=MalaisianCitySerializers

