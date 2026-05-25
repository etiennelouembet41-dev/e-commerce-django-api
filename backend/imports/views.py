from django.shortcuts import render
from rest_framework import viewsets
from .models import ImportInfo
from .serializers import ImportInfoSerializers
# Create your views here.

class ImportInfoViewsets(viewsets.ModelViewSet):
    queryset=ImportInfo.objects.all()
    serializer_class=ImportInfoSerializers