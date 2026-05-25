from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Order,OrderItem
from .serializers import OrderSerializers,OrderItemSerializers
# Create your views here.

class OrderViewsets(viewsets.ModelViewSet):
    serializer_class=OrderSerializers
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class OrderItemViewsets(viewsets.ModelViewSet):
    serializer_class=OrderItemSerializers
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return OrderItem.objects.filter(orders__user=self.request.user)