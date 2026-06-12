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


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .services import change_order_status

from core.models import Notification
from core.realtime import send_realtime_notification


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
            "car__origin_country",
            "delivery_city",
            "delivery_address",
        ).all()

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
        
        OrderItem.objects.create(
            orders=order,   # ou orders=order si ton champ s'appelle orders
            car=car,
            quantity=1,
            price=car_price,
        )

        send_order_confirmation_email(order)

        notification = Notification.objects.create(
            user=order.user,
            title="Commande créée",
            message=f"Votre commande #{order.id} a été créée."
        )

        send_realtime_notification(order.user, notification)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializers
    
    @action(detail=True, methods=["post"], url_path="change-status")
    def change_status(self, request, pk=None):
        order = self.get_object()

        if request.user.role != "admin":
            return Response(
                {"error": "Admin only"},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")
        note = request.data.get("note", "")

        try:
            order = change_order_status(
                order=order,
                new_status=new_status,
                user=request.user,
                note=note
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Order status updated",
            "order_id": order.id,
            "new_status": order.status,
        })


class OrderItemViewsets(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.select_related(
            "user",
            "car",
            "car__origin_country",
            "delivery_city",
            "delivery_address",
        ).all()

        print("USER:", self.request.user)
        print("USER ID:", self.request.user.id)
        print("USER ROLE:", getattr(self.request.user, "role", None))
        print("IS STAFF:", self.request.user.is_staff)
        print("TOTAL ORDERS:", queryset.count())
        print("USER ORDERS:", queryset.filter(user=self.request.user).count())

        if self.request.user.is_staff or self.request.user.role == "admin":
            return queryset

        return queryset.filter(user=self.request.user)