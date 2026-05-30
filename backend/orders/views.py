from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import Order,OrderItem
from .serializers import OrderSerializers,OrderItemSerializers, OrderDetailSerializer

from core.emails import send_order_confirmation_email
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
        
        queryset = Order.objects.select_related(
            "user",
            "car",
            "delivery_city",
            "delivery_address"
        )
        
        if self.request.user.role == "admin":
            return Order.objects.all()
        
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        #serializer.save(user=self.request.user) on modifie suite aux mails ajouté 
        car=serializer.validated_data["car"]
        delivery_city=serializer.validated_data["delivery_city"]

        import_info=getattr(car, "import_info", None)

        car_price=car.price
        import_fees=import_info.estimated_import_cost if import_info else 0
        delivery_fees=delivery_city.delivery_price
        
        total_price=car_price+import_fees+delivery_fees

        order=serializer.save(
               user=self.request.user,
               car_price=car_price,
               import_fees=import_fees,
               delivery_fees=delivery_fees,
               total_price=total_price, 
            )
        
        send_order_confirmation_email(order)
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializers
        
        
class OrderItemViewsets(viewsets.ModelViewSet):
    serializer_class=OrderItemSerializers
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return OrderItem.objects.filter(orders__user=self.request.user)
    
