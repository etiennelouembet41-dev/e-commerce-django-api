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
    
class ImportTrackingView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, order_id):
        try:
            order=Order.objects.select_related(
                "car",
                "car__import_info",
                "delivery_city",
            ).get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error":"Order not found"},
                status=404
            )
        
        import_info=order.car.import_info
        
        steps=[
            "pending",
            "confirmed",
            "supplier_purchase",
            "documents_preparation",
            "international_shipping",
            "malaysia_customs",
            "local_delivery",
            "delivered",
            
            
        ]
        
        current_index=steps.index(import_info.status)

        timeline=[]

        for index, step in enumerate(steps):
            timeline.append(
                {
                    "status":step,
                    "completed": index <= current_index,
                    "current": index == current_index,
                    
                }
            )
        
        return Response(
            {
                "order_id":order.id,
                "car":f"{order.car.brand} {order.car.model}",
                "delivery_city":order.delivery_city.name,
                "current_status": import_info.status,
                "estimated_import_days":import_info.estimated_import_days,
                "timeline":timeline,
            }
        )