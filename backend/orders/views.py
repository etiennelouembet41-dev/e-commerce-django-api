from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from .serializers import (
    OrderSerializers,
    OrderItemSerializers,
    OrderDetailSerializer,
    OrderListSerializer,
)

from imports.models import ImportInfo
from core.emails import send_order_confirmation_email
from core.models import Notification


class OrderViewsets(viewsets.ModelViewSet):
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

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
            "delivery_address",
        )

        if self.request.user.is_staff or self.request.user.role == "admin":
            return queryset

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        car = serializer.validated_data["car"]
        delivery_city = serializer.validated_data["delivery_city"]

        import_info, created = ImportInfo.objects.get_or_create(
            car=car,
            defaults={
                "estimated_import_cost": 0,
                "estimated_import_days": 45,
                "required_documents": (
                    "Invoice, Export Certificate, Bill of Lading, Customs Form"
                ),
                "customs_fees": 0,
                "status": "pending",
            },
        )

        car_price = car.price
        import_fees = import_info.estimated_import_cost
        delivery_fees = delivery_city.delivery_price
        total_price = car_price + import_fees + delivery_fees

        order = serializer.save(
            user=self.request.user,
            car_price=car_price,
            import_fees=import_fees,
            delivery_fees=delivery_fees,
            total_price=total_price,
        )

        send_order_confirmation_email(order)

        Notification.objects.create(
            user=order.user,
            title="Commande créée",
            message=f"Votre commande #{order.id} a été créée avec succès.",
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializers


class OrderItemViewsets(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = OrderItem.objects.select_related(
            "order",
            "car",
            "order__user",
        )

        if self.request.user.is_staff or self.request.user.role == "admin":
            return queryset

        return queryset.filter(order__user=self.request.user)