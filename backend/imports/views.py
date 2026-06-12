from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import ImportInfo
from .serializers import ImportInfoSerializers

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order

from core.permissions import IsAdminUserRole
# Create your views here.

class ImportInfoViewsets(viewsets.ModelViewSet):
    queryset = ImportInfo.objects.select_related(
        "car"
    ).all()
    serializer_class=ImportInfoSerializers
    permission_classes = [IsAdminUserRole]
    
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
    
class ImportTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            queryset = Order.objects.select_related(
                "user",
                "car",
                "car__origin_country",
                "delivery_city",
            )

            if request.user.is_staff or request.user.role == "admin":
                order = queryset.get(id=order_id)
            else:
                order = queryset.get(id=order_id, user=request.user)

            import_info = ImportInfo.objects.get(car=order.car)

        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=404
            )

        except ImportInfo.DoesNotExist:
            return Response(
                {"error": "Import info not found for this car"},
                status=404
            )

        steps = [
            "pending",
            "confirmed",
            "supplier_purchase",
            "documents_preparation",
            "international_shipping",
            "malaysia_customs",
            "local_delivery",
            "delivered",
        ]

        current_index = steps.index(import_info.status)

        timeline = []

        for index, step in enumerate(steps):
            timeline.append({
                "status": step,
                "completed": index <= current_index,
                "current": index == current_index,
            })

        status_remaining_days = {
            "pending": import_info.estimated_import_days,
            "confirmed": max(import_info.estimated_import_days - 5, 0),
            "supplier_purchase": max(import_info.estimated_import_days - 15, 0),
            "documents_preparation": max(import_info.estimated_import_days - 25, 0),
            "international_shipping": max(import_info.estimated_import_days - 35, 0),
            "malaysia_customs": max(import_info.estimated_import_days - 48, 0),
            "local_delivery": max(import_info.estimated_import_days - 55, 0),
            "delivered": 0,
        }

        remaining_days = status_remaining_days.get(
            import_info.status,
            import_info.estimated_import_days
        )

        progress_percent = int(
            (current_index / (len(steps) - 1)) * 100
        )

        return Response({
            "order_id": order.id,
            "car": f"{order.car.brand} {order.car.model}",
            "delivery_city": order.delivery_city.name,

            "order_status": order.status,
            "payment_status": order.payment_status,
            "current_status": import_info.status,

            "estimated_import_days": import_info.estimated_import_days,
            "remaining_days": remaining_days,
            "progress_percent": progress_percent,

            "timeline": timeline,
        })