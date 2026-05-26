from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import Car, CarImage
from .serializers import CarSerializers,CarImageSerializers

from core.permissions import IsAdminOrReadOnly

# Create your views here.


class CarViewsets(viewsets.ModelViewSet):
    queryset=Car.objects.all()
    serializer_class=CarSerializers
    permission_classes=[IsAdminOrReadOnly]
    
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    
    filterest_fields=(
        "brand",
        "origin_country",
        "race_type",
        "conditions",
        "transmission",
        "fuel",
        "is_available",
        
    )
    
    search_fields=(
        "brand",
        "model",
        "description",
    )
    
    ordering_fields=( 
        "price",
        "year",
        "power_hp",
        "mileage",
        "created_at",
    )
    
class CarImageViewsets(viewsets.ModelViewSet):
    queryset=CarImage.objects.all()
    serializer_class=CarImageSerializers
    