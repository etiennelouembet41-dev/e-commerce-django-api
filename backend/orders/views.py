from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import Order,OrderItem
from .serializers import OrderSerializers,OrderItemSerializers
# Create your views here.

class OrderViewsets(viewsets.ModelViewSet):
    serializer_class=OrderSerializers
    permission_classes=[IsAuthenticated]
    
    filterset_fields = (
            "status",
            "payment_status",
            "delivery_city",
            "created_at",
        )

    search_fields = (
        "user__email",
        "car__brand",
        "car__model",
        "stripe_payment_id",
    )

    ordering_fields = (
        "created_at",
        "total_price",
    )

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class OrderItemViewsets(viewsets.ModelViewSet):
    serializer_class=OrderItemSerializers
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return OrderItem.objects.filter(orders__user=self.request.user)