from django.shortcuts import render

from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from cars.models import Car
from ai_assistant.models import AIQuestion
from imports.models import ImportInfo
# Create your views here.


class DashboardStatsView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        
        total_ai_questions=AIQuestion.objects.count()

        frequent_ai_questions=(
            AIQuestion.objects.values("question")
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
        )
        
        most_recommended_cars=(
            AIQuestion.objects.values(
                "recommended_cars__brand",
                "recommended_cars__model"
                
            )
            .exclude(recommended_cars=None)
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
            
        )
        
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
                
                "total_ai_questions":total_ai_questions,
                "frequent_ai_questions":frequent_ai_questions,
                "most_recommended_cars":most_recommended_cars,
                
            }
        )