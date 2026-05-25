from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import ImportInfo
from .serializers import ImportInfoSerializers
# Create your views here.

class ImportInfoViewsets(viewsets.ModelViewSet):
    queryset=ImportInfo.objects.all()
    serializer_class=ImportInfoSerializers
    
    filterset_fields = (
        "status",
        "car__origin_country",
        "car__race_type",
    )

    search_fields = (
        "car__brand",
        "car__model",
        "required_documents",
    )

    ordering_fields = (
        "estimated_import_cost",
        "estimated_import_days",
        "updated_at",
    )