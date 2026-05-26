from django.shortcuts import render

from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from cars.models import Car
from imports.models import ImportInfo
# Create your views here.


class DashboardStatsView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        
        total_revenue=(
            Order.objects.filter(payment_status="paid").aggregate(total=Sum("total_price"))
        )
        
        total_orders=Order.objects.count()

        available_cars=Car.objects.filter(
            is_available=True
        ).count()

        sold_cars=Car.objects.filter(
            is_sold=True
        ).count()

        importing_cars=ImportInfo.objects.exclude(
            status="delivered"
        ).count()

        monthly_sales=(
            Order.objects.filter(payment_status="paid")
                .annotate(month=TruncMonth("created_at"))
                .values("month")
                .annotate(total=Sum("total_price"))
                .order_by("month")
        )
        
        sales_by_city=(
            Order.objects.values("delivery_city__city__name") 
                .annotate(total=Count("id"))
                .order_by("-total")
        )
        
        return Response(
            {
                "total_revenue":total_revenue,
                "total_orders":total_orders,
                "available_cars":available_cars,
                "sold_cars":sold_cars,
                "importing_cars":importing_cars,
                "monthly_sales":monthly_sales,
                "sales_by_city":sales_by_city,
                
            }
        )