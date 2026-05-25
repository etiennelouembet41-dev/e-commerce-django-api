from django.shortcuts import render
from rest_framework import viewsets
from .models import Car, CarImage
from .serializers import CarSerializers,CarImageSerializers
# Create your views here.


class CarViewsets(viewsets.ModelViewSet):
    queryset=Car.objects.all()
    serializer_class=CarSerializers
    
class CarImageViewsets(viewsets.ModelViewSet):
    queryset=CarImage.objects.all()
    serializer_class=CarImageSerializers
    